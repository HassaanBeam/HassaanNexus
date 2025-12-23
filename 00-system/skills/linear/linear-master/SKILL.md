---
name: linear-master
description: Shared resource library for Linear integration skills. DO NOT load directly - provides common references (setup, API docs, error handling, authentication) and scripts used by linear-create-tickets, linear-update-tickets, and related skills.
---

# Linear Master Skill

## Overview

This is a **shared resource library** for all Linear-related skills. It is NOT executed directly.

## Provides

### References
- [Authentication](references/authentication.md) - API key setup and usage
- [API Reference](references/api-reference.md) - GraphQL queries and mutations
- [Team Reference](references/teams.md) - Team IDs and state mappings

### Scripts
- `scripts/linear_client.py` - Reusable GraphQL client with error handling
- `scripts/list_issues.py` - Query issues with filters
- `scripts/create_issue.py` - Create new issues
- `scripts/update_issue.py` - Update issue status/fields

## Used By

- `03-skills/linear-create-tickets` - Create tickets from action items
- `03-skills/linear-update-tickets` - Update ticket status
- `03-skills/create-weekly-update` - Generate weekly status
- `03-skills/process-client-meeting` - Meeting processing workflow

## Configuration

Requires `.env` file at project root with:
```
LINEAR_API_KEY=lin_api_xxxxx
```

## API Endpoint

```
https://api.linear.app/graphql
```

**Important**: Linear uses GraphQL. All operations are POST requests to the single GraphQL endpoint.
