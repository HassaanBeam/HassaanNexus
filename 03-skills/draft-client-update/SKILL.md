---
name: draft-client-update
description: Generate an external client-facing update message for Slack or email. Load when user says "draft client update", "create client summary", "external update message", "client message after meeting", "prepare summary for client", or "write client email". Returns a draft for review before sending.
---

# Draft Client Update

Generate external client-facing summary message.

## Workflow

### Step 1: Gather Information

Collect:
- Meeting/discussion summary
- Key points covered
- Next steps
- Client action items
- Next meeting date (if scheduled)
- Recording/document links

### Step 2: Determine Format

**Slack** (default):
- Emoji headers
- Casual but professional tone
- Bullet points

**Email**:
- Formal structure
- Subject line
- Professional sign-off

### Step 3: Generate Draft

**Slack Format**:
```
Hi team! Great [call type] today. Here's a summary:

📝 *Summary*
[2-3 sentence overview]

✅ *What We Covered*
• [Topic 1]
• [Topic 2]
• [Topic 3]

🎯 *Next Steps*
• [Action] - @[person]
• [Action] - @[person]

📅 *Next Session*
[Day, Date at Time]

📋 *Meeting minutes*
[Link]

📺 *Recording*
[Link]

❓ *Questions?*
Drop them here!
```

**Email Format**:
```
Subject: Meeting Summary - [Date]

Hi [Name/Team],

Thank you for the meeting today. Here's a summary:

## Key Discussion Points
• [Point 1]
• [Point 2]

## Decisions Made
• [Decision]

## Action Items
• [Action] - [Person] - Due: [Date]

## Next Steps
• [Step]

## Next Meeting
[Date/Time]

Please reach out with any questions.

Best regards,
[Name]
```

### Step 4: Review Checkpoint

**IMPORTANT**: Always present draft for approval before sending.

```
Here's the draft:
---
[Content]
---

Options:
1. Approve as-is
2. Request changes
3. Discard
```

---

## Key Principles

- Professional but friendly tone
- Focus on value and next steps
- Client actions prominently displayed
- No internal jargon
- Clear call-to-action

---

## Output

Returns draft content and metadata:
```json
{
  "format": "slack",
  "content": "...",
  "status": "pending_approval"
}
```

---

## Related Skills

- `create-meeting-minutes` - Source content
- `send-internal-update` - Internal version
- `process-client-meeting` - Full workflow
