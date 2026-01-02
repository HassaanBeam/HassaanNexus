#!/usr/bin/env python3
"""
Beam.ai API Client

Shared client for interacting with Beam.ai API.
Supports both BID (staging) and Production workspaces.
"""

import os
from pathlib import Path
from typing import Optional

import requests
from dotenv import load_dotenv


# Workspace configurations
WORKSPACES = {
    "bid": {
        "base_url": "https://api.bid.beamstudio.ai",
        "api_key_env": "BEAM_API_KEY",
        "workspace_id_env": "BEAM_WORKSPACE_ID"
    },
    "prod": {
        "base_url": "https://api.beamstudio.ai",
        "api_key_env": "BEAM_API_KEY_PROD",
        "workspace_id_env": "BEAM_WORKSPACE_ID_PROD"
    }
}


def find_project_root() -> Path:
    """Find project root by looking for CLAUDE.md or .git directory."""
    current = Path(__file__).resolve().parent
    for _ in range(10):
        if (current / "CLAUDE.md").exists() or (current / ".git").exists():
            return current
        if current.parent == current:
            break
        current = current.parent
    return Path(__file__).resolve().parent.parent.parent


class BeamClient:
    """
    Client for Beam.ai API.

    Usage:
        client = BeamClient(workspace='prod')
        tasks = client.get('/agent-tasks', params={'agentId': '...'})
    """

    def __init__(self, workspace: str = "bid"):
        """
        Initialize Beam API client.

        Args:
            workspace: 'bid' for staging, 'prod' for production
        """
        if workspace not in WORKSPACES:
            raise ValueError(f"Unknown workspace: {workspace}. Use 'bid' or 'prod'")

        # Load .env from project root
        env_path = find_project_root() / ".env"
        load_dotenv(env_path)

        config = WORKSPACES[workspace]
        self.base_url = config["base_url"]
        self.workspace = workspace

        # Get credentials
        self.api_key = os.getenv(config["api_key_env"])
        self.workspace_id = os.getenv(config["workspace_id_env"])

        if not self.api_key:
            raise ValueError(f"{config['api_key_env']} not found in environment")
        if not self.workspace_id:
            raise ValueError(f"{config['workspace_id_env']} not found in environment")

    def _get_headers(self) -> dict:
        """Get headers for API requests."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "current-workspace-id": self.workspace_id,
            "Content-Type": "application/json"
        }

    def get(self, endpoint: str, params: Optional[dict] = None) -> dict:
        """
        Make GET request to Beam API.

        Args:
            endpoint: API endpoint (e.g., '/agent-tasks')
            params: Query parameters

        Returns:
            JSON response as dict
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self._get_headers(), params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: Optional[dict] = None) -> dict:
        """
        Make POST request to Beam API.

        Args:
            endpoint: API endpoint
            data: Request body

        Returns:
            JSON response as dict (or empty dict for 201 responses)
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, headers=self._get_headers(), json=data)
        response.raise_for_status()

        # Handle empty responses (e.g., 201 Created)
        if response.status_code == 201 and not response.text:
            return {}

        return response.json()

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Make raw request to Beam API.

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional arguments for requests

        Returns:
            Raw response object
        """
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("headers", self._get_headers())
        response = requests.request(method, url, **kwargs)
        return response
