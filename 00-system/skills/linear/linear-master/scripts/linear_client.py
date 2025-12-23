#!/usr/bin/env python3
"""
Linear API Client

Shared client for Linear GraphQL API authentication and requests.
Used by all Linear API scripts.
"""

import os
import time
import logging
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
GRAPHQL_ENDPOINT = "https://api.linear.app/graphql"


class LinearError(Exception):
    """Custom exception for Linear API errors."""

    def __init__(self, message, errors=None):
        self.message = message
        self.errors = errors or []
        super().__init__(f"Linear API Error: {message}")


class LinearClient:
    """Linear GraphQL API client with automatic error handling and retry logic."""

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

        self.api_key = env_vars.get('LINEAR_API_KEY') or os.getenv('LINEAR_API_KEY')

        if not self.api_key:
            raise ValueError("LINEAR_API_KEY not found in .env or environment")

    def get_headers(self):
        """Get headers for API request. Note: Linear uses key directly, NOT Bearer."""
        return {
            'Authorization': self.api_key,  # NOT Bearer!
            'Content-Type': 'application/json'
        }

    def _execute(self, query, variables=None, max_retries=3):
        """Execute GraphQL query with automatic retry for rate limits."""
        import requests

        payload = {'query': query}
        if variables:
            payload['variables'] = variables

        for attempt in range(max_retries):
            try:
                response = requests.post(
                    GRAPHQL_ENDPOINT,
                    headers=self.get_headers(),
                    json=payload,
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

                result = response.json()

                # Check for GraphQL errors
                if 'errors' in result:
                    errors = result['errors']
                    messages = [e.get('message', str(e)) for e in errors]
                    raise LinearError('; '.join(messages), errors=errors)

                return result.get('data', {})

            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise LinearError("Request timeout")
            except requests.exceptions.ConnectionError:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise LinearError("Cannot connect to Linear API")

        raise LinearError("Max retries exceeded")

    def query(self, query, variables=None):
        """Execute a GraphQL query."""
        return self._execute(query, variables)

    def mutate(self, mutation, variables=None):
        """Execute a GraphQL mutation."""
        return self._execute(mutation, variables)

    # Convenience methods

    def get_viewer(self):
        """Get current user info."""
        query = """
        query {
          viewer {
            id
            name
            email
          }
        }
        """
        return self.query(query).get('viewer', {})

    def list_issues(self, project_name=None, states=None, limit=50):
        """
        List issues with optional filters.

        Args:
            project_name: Filter by project name
            states: List of state names (e.g., ["Todo", "In Progress"])
            limit: Max results
        """
        filters = []

        if project_name:
            filters.append(f'project: {{ name: {{ eq: "{project_name}" }} }}')

        if states:
            state_list = ', '.join(f'"{s}"' for s in states)
            filters.append(f'state: {{ name: {{ in: [{state_list}] }} }}')

        filter_str = ', '.join(filters)
        if filter_str:
            filter_str = f'filter: {{ {filter_str} }}'

        query = f"""
        query {{
          issues({filter_str}, first: {limit}) {{
            nodes {{
              id
              identifier
              title
              state {{ id name }}
              assignee {{ name }}
              priority
              description
              createdAt
              updatedAt
            }}
          }}
        }}
        """
        return self.query(query).get('issues', {}).get('nodes', [])

    def create_issue(self, title, team_id, description=None, project_id=None,
                     state_id=None, priority=None, assignee_id=None):
        """
        Create a new issue.

        Args:
            title: Issue title (required)
            team_id: Team UUID (required)
            description: Issue description
            project_id: Project UUID
            state_id: Initial state UUID
            priority: Priority (1=Urgent, 2=High, 3=Medium, 4=Low)
            assignee_id: Assignee user UUID
        """
        mutation = """
        mutation CreateIssue($input: IssueCreateInput!) {
          issueCreate(input: $input) {
            success
            issue {
              id
              identifier
              title
              state { name }
            }
          }
        }
        """

        input_data = {
            'title': title,
            'teamId': team_id
        }

        if description:
            input_data['description'] = description
        if project_id:
            input_data['projectId'] = project_id
        if state_id:
            input_data['stateId'] = state_id
        if priority:
            input_data['priority'] = priority
        if assignee_id:
            input_data['assigneeId'] = assignee_id

        result = self.mutate(mutation, {'input': input_data})
        return result.get('issueCreate', {})

    def update_issue(self, issue_id, state_id=None, priority=None, assignee_id=None):
        """
        Update an existing issue.

        Args:
            issue_id: Issue UUID (required)
            state_id: New state UUID
            priority: New priority
            assignee_id: New assignee UUID
        """
        mutation = """
        mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
          issueUpdate(id: $id, input: $input) {
            success
            issue {
              id
              identifier
              title
              state { name }
            }
          }
        }
        """

        input_data = {}
        if state_id:
            input_data['stateId'] = state_id
        if priority is not None:
            input_data['priority'] = priority
        if assignee_id:
            input_data['assigneeId'] = assignee_id

        if not input_data:
            raise ValueError("At least one field must be specified for update")

        result = self.mutate(mutation, {'id': issue_id, 'input': input_data})
        return result.get('issueUpdate', {})

    def add_comment(self, issue_id, body):
        """
        Add a comment to an issue.

        Args:
            issue_id: Issue UUID
            body: Comment text (supports markdown)
        """
        mutation = """
        mutation AddComment($issueId: String!, $body: String!) {
          commentCreate(input: {
            issueId: $issueId,
            body: $body
          }) {
            success
            comment {
              id
              body
            }
          }
        }
        """
        result = self.mutate(mutation, {'issueId': issue_id, 'body': body})
        return result.get('commentCreate', {})


def get_client():
    """Get a configured Linear client."""
    return LinearClient()


if __name__ == "__main__":
    # Test the client
    import json

    try:
        client = get_client()
        print("Linear client initialized successfully")

        # Test getting viewer
        viewer = client.get_viewer()
        print(f"Connected as: {viewer.get('name')} ({viewer.get('email')})")

    except ValueError as e:
        print(f"Configuration error: {e}")
    except LinearError as e:
        print(f"API error: {e}")
