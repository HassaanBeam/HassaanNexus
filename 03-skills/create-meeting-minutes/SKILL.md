---
name: create-meeting-minutes
description: Transform a meeting transcript into formatted meeting minutes. Load when user says "create meeting minutes", "format meeting notes", "generate minutes from transcript", "meeting minutes from recording", or provides a transcript to format. Extracts discussion points, action items, and creates structured documentation.
---

# Create Meeting Minutes

Transform meeting transcript into formatted meeting minutes.

## Workflow

### Step 1: Get Transcript

Accept from:
1. Output from `fathom-fetch-meetings`
2. User-pasted transcript text
3. File path to transcript

### Step 2: Extract Information

**Discussion Points** (non-action items):
- Key topics discussed
- Technical details explained
- Decisions made
- Blockers or dependencies mentioned

**Action Items**:
- Tasks with clear deliverables
- Assignee (who is responsible)
- Due dates (if mentioned)
- Categorize by team (internal vs external)

**Metadata**:
- Date
- Attendees (from speakers)
- Meeting type/topic

### Step 3: Format Minutes

```markdown
# Meeting Minutes: [Parties] — [Topic]

**Date:** [Month Day, Year]

**Attendees:** [Name] (Company), [Name] (Company)

**Recording:** [Link if available]

---

## Discussion Points

- [Topic with context and any decisions made]
- [Another discussion point]
- [Technical details or process explanations]
- [Blockers, dependencies, or waiting items]

---

## Action Points

- [Person] to [specific task with clear deliverable]
- [Person] to [specific task with clear deliverable]
```

### Step 4: Save (Optional)

If save location specified:
```
[project-folder]/meetings/YYYY-MM-DD-Meeting-Minutes.md
```

### Step 5: Return Action Items

Separate action items by owner for downstream use:
- **Internal team actions** → For ticket creation
- **External/client actions** → For client communication

---

## Action Item Extraction Rules

**Include**:
- Tasks with specific deliverables
- Tasks with clear ownership
- Follow-up items with deadlines

**Exclude**:
- "Set up next meeting" (scheduling tasks)
- Vague items without deliverables
- Already completed items

---

## Output

```json
{
  "file_saved": "path/to/minutes.md",
  "date": "2025-12-15",
  "attendees": [...],
  "discussion_points": [...],
  "action_items": {
    "internal": [...],
    "external": [...]
  }
}
```

---

## Related Skills

- `fathom-fetch-meetings` - Source transcripts
- `linear-create-tickets` - Create tickets from action items
- `process-client-meeting` - Full workflow
