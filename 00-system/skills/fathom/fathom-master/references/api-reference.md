# Fathom API Reference

## Base URL

```
https://api.fathom.ai/external/v1
```

---

## Endpoints

### List Meetings

**GET** `/meetings`

Returns a list of recorded meetings.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `calendar_invitees_domains[]` | string | Filter by attendee email domain (e.g., `smartly.io`) |
| `include_summary` | boolean | Include AI-generated summary |
| `include_transcript` | boolean | Include full transcript |
| `include_action_items` | boolean | Include extracted action items |
| `created_after` | string | ISO 8601 date (e.g., `2025-01-01T00:00:00Z`) |
| `created_before` | string | ISO 8601 date |
| `limit` | integer | Max results per page (default: 50) |
| `cursor` | string | Pagination cursor from previous response |

**Example:**
```bash
curl -s --request GET \
  --url 'https://api.fathom.ai/external/v1/meetings?calendar_invitees_domains[]=smartly.io&include_summary=true' \
  --header 'X-Api-Key: YOUR_API_KEY'
```

**Response:**
```json
{
  "items": [
    {
      "id": "meeting-id",
      "title": "Weekly Sync",
      "created_at": "2025-01-15T10:00:00Z",
      "duration_seconds": 3600,
      "recording_id": 123456789,
      "calendar_invitees": [
        {
          "email": "user@smartly.io",
          "display_name": "User Name"
        }
      ],
      "summary": "Discussion about...",
      "action_items": [
        {"text": "Action item 1", "assignee": "User Name"}
      ]
    }
  ],
  "next_cursor": "cursor-for-next-page",
  "limit": 50
}
```

---

### Get Transcript

**GET** `/recordings/{recording_id}/transcript`

Returns the full transcript for a specific recording.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `recording_id` | string | UUID of the recording |

**Example:**
```bash
curl -s --request GET \
  --url 'https://api.fathom.ai/external/v1/recordings/RECORDING_ID/transcript' \
  --header 'X-Api-Key: YOUR_API_KEY'
```

**Response:**
```json
{
  "transcript": [
    {
      "speaker": {
        "display_name": "Speaker Name",
        "matched_calendar_invitee_email": "email@domain.com"
      },
      "text": "What they said",
      "timestamp": "00:01:23"
    }
  ]
}
```

---

### Get Recording Details

**GET** `/recordings/{recording_id}`

Returns metadata about a specific recording.

**Response:**
```json
{
  "id": "recording-uuid",
  "meeting_id": "meeting-uuid",
  "duration_seconds": 3600,
  "created_at": "2025-01-15T10:00:00Z",
  "status": "ready"
}
```

---

## Rate Limits

- **60 requests per 60 seconds** (global limit)
- 429 response indicates rate limiting - wait and retry
- Response headers:
  - `RateLimit-Limit`: Max requests in window
  - `RateLimit-Remaining`: Requests left
  - `RateLimit-Reset`: Time until window resets

---

## Common Patterns

### Filter by Client Domain
```python
params = {
    "calendar_invitees_domains[]": "smartly.io",
    "include_summary": "true",
    "include_action_items": "true"
}
```

### Fetch Meetings from Last 7 Days
```python
from datetime import datetime, timedelta

week_ago = (datetime.now() - timedelta(days=7)).isoformat() + "Z"
params = {
    "created_after": week_ago
}
```
