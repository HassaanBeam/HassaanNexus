---
name: send-internal-update
description: Send an internal team update to Slack after a meeting or discussion. Load when user says "send internal update", "post to team channel", "internal meeting summary", "share notes with team", "post update internally". Formats and posts to specified Slack channel.
---

# Send Internal Update

Post internal team update to Slack.

## Workflow

### Step 1: Gather Information

Collect:
- Context (client/project name, meeting type)
- Summary of discussion
- Key decisions made
- Blockers (if any)
- Team action items with owners
- Link to full notes

### Step 2: Format Message

**Internal Template**:
```
Hi team! Just wrapped up [call type] with [context]. Here are the notes:

:memo: Summary
[2-3 sentence overview of outcomes]

:white_check_mark: Decisions
• [Decision 1]
• [Decision 2]

:construction: Blockers
• [Blocker] (or "None")

:dart: Action Items
• @[person]: [Task] - Due: [Date]
• @[person]: [Task] - Due: [Date]

Full notes: [Link]
```

### Step 3: Identify Channel

Options:
- User specifies: "#team-channel"
- Default internal channel
- Project-specific channel

### Step 4: Send Message

Use Slack API or MCP:
```bash
# Via Slack API
curl -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer {BOT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"channel": "CHANNEL_ID", "text": "...", "mrkdwn": true}'
```

### Step 5: Confirm

```
Internal update posted to #[channel]
Timestamp: [ts]
```

---

## Differences from Client Update

| Internal | Client |
|----------|--------|
| Technical details OK | No jargon |
| @mentions for team | @mentions for their team |
| Blockers section | Progress focus |
| Links to internal docs | Public links only |
| Casual tone | Professional tone |

---

## Channel Configuration

Can configure default channels:
- Per-project internal channel
- Team-wide updates channel
- Specific topic channels

---

## Related Skills

- `draft-client-update` - External version
- `create-meeting-minutes` - Source content
- `process-client-meeting` - Full workflow
