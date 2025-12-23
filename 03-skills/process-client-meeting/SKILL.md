---
name: process-client-meeting
description: Complete workflow to process a meeting end-to-end. Load when user says "process meeting", "meeting workflow", "process client meeting", "full meeting processing", "handle meeting for [client]", or "post-meeting workflow". Orchestrates fetching transcripts, creating minutes, Linear tickets, drafting updates, sending internal updates, and updating project context.
---

# Process Client Meeting

**CONSOLIDATED WORKFLOW**: Orchestrates multiple skills for complete meeting processing.

## Overview

This workflow chains:
1. `fathom-fetch-meetings` → Fetch meeting transcript
2. `create-meeting-minutes` → Format into minutes
3. `linear-create-tickets` → Create tickets for action items
4. `linear-update-tickets` → Update tickets discussed in meeting
5. `draft-client-update` → Generate external message
6. `send-internal-update` → Post to team channel
7. `update-project-context` → Sync project files

---

## Workflow Execution

### STEP 1: Fetch Meeting
**Uses**: `fathom-fetch-meetings`

Get meeting from Fathom filtered by domain:
```
Fetching meetings for [domain]...

Found 3 meetings:
1. Weekly Sync - Dec 15, 2025
2. POC Review - Dec 12, 2025
3. Technical Deep-Dive - Dec 10, 2025
```

**CHECKPOINT**: Ask user which meeting to process.

---

### STEP 2: Create Meeting Minutes
**Uses**: `create-meeting-minutes`

Fetch full transcript and parse into structured minutes:
- Discussion points
- Action items (categorized by owner)
- Decisions made

Save to: `[project]/meetings/YYYY-MM-DD-Meeting-Minutes.md`

---

### STEP 3: Create Linear Tickets
**Uses**: `linear-create-tickets`

For each internal team action item:
- Filter out scheduling tasks
- Create ticket in appropriate project
- Assign default owner

```
Created 3 tickets:
- CLI-456: Implement validation
- CLI-457: Update documentation
- CLI-458: Review architecture
```

---

### STEP 4: Update Existing Tickets
**Uses**: `linear-update-tickets`

If meeting discussed existing work:
- Identify tickets mentioned
- Update status if completed
- Add comments with context

```
Tickets mentioned in meeting:
- CLI-400: "Pipeline setup" - discussed as complete

Mark CLI-400 as Done? (y/n)
```

---

### STEP 5: Draft Client Update
**Uses**: `draft-client-update`

Generate external-facing summary:
- Meeting overview
- What was covered
- Next steps and action items
- Next meeting date

**CHECKPOINT**: Present draft for approval before proceeding.

```
Draft client update:
---
[Content]
---

1. Approve and continue
2. Request changes
3. Skip client update
```

---

### STEP 6: Send Internal Update
**Uses**: `send-internal-update`

Post to internal team channel:
- Summary and decisions
- Blockers
- Team action items
- Link to full notes

---

### STEP 7: Update Project Context
**Uses**: `update-project-context`

Sync project files:
- Add entry to PROJECT_CONTEXT.md
- Update project-state.json
- Capture decisions and action items

---

## Completion Summary

```
✅ Meeting Processing Complete

📋 Meeting Minutes
   Saved: [path]

🎫 Linear Tickets
   Created: CLI-456, CLI-457, CLI-458
   Updated: CLI-400 → Done

📤 Client Update
   Status: [approved/pending/skipped]

📢 Internal Update
   Posted to: #[channel]

📁 Project Context
   Updated: PROJECT_CONTEXT.md, project-state.json

Would you like to send the client update now?
```

---

## Error Handling

If any step fails:
1. Report which step failed and why
2. Offer to retry or skip
3. Continue with remaining steps
4. Summarize success/failure at end

---

## HITL Checkpoints

Two mandatory checkpoints for human approval:
1. **After Step 1**: Select which meeting to process
2. **After Step 5**: Approve client update before sending

---

## Customization

Each step can be run independently:
- Skip Fathom fetch if transcript provided
- Skip ticket creation if no action items
- Skip client update if internal-only meeting

---

## Skills Used

| Step | Skill | Purpose |
|------|-------|---------|
| 1 | `fathom-fetch-meetings` | Get transcript |
| 2 | `create-meeting-minutes` | Format minutes |
| 3 | `linear-create-tickets` | Create new tickets |
| 4 | `linear-update-tickets` | Update existing |
| 5 | `draft-client-update` | External message |
| 6 | `send-internal-update` | Team notification |
| 7 | `update-project-context` | Sync files |
