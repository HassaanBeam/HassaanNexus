#!/usr/bin/env python3
"""
Fathom API Client

Shared client for Fathom API authentication and requests.
Used by all Fathom API scripts.
"""

import os
import time
import logging
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
BASE_URL = "https://api.fathom.ai/external/v1"


class FathomError(Exception):
    """Custom exception for Fathom API errors."""

    def __init__(self, status_code, message, details=None):
        self.status_code = status_code
        self.message = message
        self.details = details or {}
        super().__init__(f"Fathom API Error ({status_code}): {message}")


class FathomClient:
    """Fathom API client with automatic error handling and retry logic."""

    def __init__(self):
        self.api_key = None
        self._load_config()

    def _load_config(self):
        """Load configuration from .env file."""
        env_vars = {}
        if ENV_FILE.exists():
            with open(ENV_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, _, value = line.partition('=')
                        env_vars[key.strip()] = value.strip().strip('"\'')

        self.api_key = env_vars.get('FATHOM_API_KEY') or os.getenv('FATHOM_API_KEY')

        if not self.api_key:
            raise ValueError("FATHOM_API_KEY not found in .env or environment")

    def get_headers(self):
        """Get headers for API request."""
        return {
            'X-Api-Key': self.api_key,
            'Content-Type': 'application/json'
        }

    def _handle_response(self, response):
        """Handle API response with error parsing."""
        if response.status_code == 200:
            try:
                return response.json()
            except:
                return {"status": "success"}
        else:
            try:
                error_data = response.json()
            except:
                error_data = {"message": response.text}

            raise FathomError(
                status_code=response.status_code,
                message=error_data.get('message', error_data.get('error', 'Unknown error')),
                details=error_data
            )

    def _request_with_retry(self, method, endpoint, params=None, data=None, max_retries=3):
        """Make request with automatic retry for rate limits and server errors."""
        import requests

        url = f"{BASE_URL}{endpoint}"

        for attempt in range(max_retries):
            try:
                response = requests.request(
                    method,
                    url,
                    headers=self.get_headers(),
                    params=params,
                    json=data,
                    timeout=60
                )

                # Rate limited - retry with backoff
                if response.status_code == 429:
                    wait = int(response.headers.get('Retry-After', 2 ** attempt))
                    logging.warning(f"Rate limited, waiting {wait}s")
                    time.sleep(wait)
                    continue

                # Server error - retry with backoff
                if response.status_code >= 500:
                    time.sleep(2 ** attempt)
                    continue

                return self._handle_response(response)

            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise FathomError(408, "Request timeout")
            except requests.exceptions.ConnectionError:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise FathomError(503, "Cannot connect to Fathom API")

        raise FathomError(500, "Max retries exceeded")

    def get(self, endpoint, params=None):
        """Make GET request."""
        return self._request_with_retry('GET', endpoint, params=params)

    def list_meetings(self, domain=None, include_summary=True, include_action_items=True,
                      created_after=None, created_before=None, limit=50):
        """
        List meetings with optional filters.

        Args:
            domain: Filter by attendee email domain (e.g., 'smartly.io')
            include_summary: Include AI-generated summary
            include_action_items: Include extracted action items
            created_after: ISO 8601 date string
            created_before: ISO 8601 date string
            limit: Max results per request
        """
        params = {
            'include_summary': str(include_summary).lower(),
            'include_action_items': str(include_action_items).lower(),
            'limit': limit
        }

        if domain:
            params['calendar_invitees_domains[]'] = domain
        if created_after:
            params['created_after'] = created_after
        if created_before:
            params['created_before'] = created_before

        return self.get('/meetings', params=params)

    def get_transcript(self, recording_id):
        """
        Get full transcript for a recording.

        Args:
            recording_id: UUID of the recording
        """
        return self.get(f'/recordings/{recording_id}/transcript')

    def get_recording(self, recording_id):
        """
        Get recording metadata.

        Args:
            recording_id: UUID of the recording
        """
        return self.get(f'/recordings/{recording_id}')


def get_client():
    """Get a configured Fathom client."""
    return FathomClient()


if __name__ == "__main__":
    # Test the client
    import json

    try:
        client = get_client()
        print("Fathom client initialized successfully")

        # Test listing meetings
        result = client.list_meetings(limit=5)
        print(f"Found {len(result.get('meetings', []))} meetings")

    except ValueError as e:
        print(f"Configuration error: {e}")
    except FathomError as e:
        print(f"API error: {e}")
