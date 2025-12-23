---
name: fathom-fetch-meetings
description: Fetch meeting recordings and transcripts from Fathom API filtered by attendee email domain. Load when user says "fetch meetings", "get fathom recordings", "fathom meetings for [domain]", "list meetings from fathom", "get transcripts", or mentions Fathom. Returns meeting summaries, action items, and optionally full transcripts.
---

# Fathom Fetch Meetings

Fetch meetings from Fathom API filtered by attendee domain.

## Configuration

**API Endpoint**: `https://api.fathom.ai/external/v1`

**API Key Location**: User must provide or store in environment/config.

**Known Domains** (expandable):
- `smartly.io` → Smartly
- `rivertrace.com` → Rivertrace

---

## Workflow

### Step 1: Get Domain

If user provides client name, map to domain:
```
"Smartly" → smartly.io
"Rivertrace" → rivertrace.com
```

If unknown, ask user for the email domain directly.

### Step 2: Fetch Meetings

```bash
curl -s --request GET \
  --url 'https://api.fathom.ai/external/v1/meetings?calendar_invitees_domains[]={DOMAIN}&include_summary=true' \
  --header 'X-Api-Key: {API_KEY}'
```

**Query Parameters**:
| Parameter | Description |
|-----------|-------------|
| `calendar_invitees_domains[]` | Filter by attendee email domain |
| `include_summary` | Include AI-generated summary |
| `include_transcript` | Include full transcript |
| `include_action_items` | Include extracted action items |
| `created_after` | ISO 8601 date filter |

### Step 3: Display Results

```
Found {count} meetings for {domain}:

1. {title} - {date}
   Summary: {preview}
   Recording ID: {id}

2. {title} - {date}
   ...
```

### Step 4: Fetch Transcript (Optional)

For specific meeting:
```bash
curl -s --request GET \
  --url 'https://api.fathom.ai/external/v1/recordings/{RECORDING_ID}/transcript' \
  --header 'X-Api-Key: {API_KEY}'
```

**Transcript Response**:
```json
{
  "transcript": [
    {
      "speaker": {"display_name": "Name", "matched_calendar_invitee_email": "email"},
      "text": "What they said",
      "timestamp": "HH:MM:SS"
    }
  ]
}
```

---

## Output

Returns meeting data including:
- Meeting title, date, duration
- AI-generated summary
- Action items with assignees
- Attendee list
- Full transcript (if requested)

---

## Related Skills

- `create-meeting-minutes` - Format transcript into minutes
- `process-client-meeting` - Full meeting workflow
