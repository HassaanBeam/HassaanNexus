---
name: fathom-master
description: Shared resource library for Fathom integration skills. DO NOT load directly - provides common references (setup, API docs, error handling, authentication) and scripts used by fathom-fetch-meetings and related skills.
---

# Fathom Master Skill

## Overview

This is a **shared resource library** for all Fathom-related skills. It is NOT executed directly.

## Provides

### References
- [Authentication](references/authentication.md) - API key setup and usage
- [API Reference](references/api-reference.md) - Endpoints and parameters
- [Error Handling](references/error-handling.md) - Common errors and solutions

### Scripts
- `scripts/fathom_client.py` - Reusable API client with error handling
- `scripts/list_meetings.py` - List meetings with filters
- `scripts/get_transcript.py` - Fetch full transcript by recording ID

## Used By

- `03-skills/fathom-fetch-meetings` - Fetch and filter meetings
- `03-skills/process-client-meeting` - Meeting processing workflow

## Configuration

Requires `.env` file at project root with:
```
FATHOM_API_KEY=your-api-key-here
```

## API Base URL

```
https://api.fathom.ai/external/v1
```
