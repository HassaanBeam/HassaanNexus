---
name: update-project-context
description: Update project context files (PROJECT_CONTEXT.md, project-state.json) with latest information. Load when user says "update project context", "sync project state", "refresh context", "save project changes", "update project files". User-triggered skill to keep project documentation current.
---

# Update Project Context

Sync project context files with latest information.

## Workflow

### Step 1: Identify Project

If not clear from context, ask:
- "Which project's context should I update?"

Locate project folder and context files:
- `PROJECT_CONTEXT.md` - Chronological update log
- `project-state.json` - Structured state data

### Step 2: Gather Updates

Information to capture:
- Recent meeting/activity date
- Summary of what happened
- New action items
- Completed tasks
- Milestone updates
- New blockers or resolved blockers
- Key decisions made
- Links to related documents

### Step 3: Update PROJECT_CONTEXT.md

Add new entry at TOP (reverse chronological):

```markdown
## [YYYY-MM-DD]

**Summary:**
[What happened - meeting, milestone, decision]

**Changes:**
- [Change 1]
- [Change 2]

**Links:**
- [Related meeting minutes]
- [Updated documents]

---

[Previous entries below...]
```

### Step 4: Update project-state.json

Update relevant fields:
```json
{
  "lastUpdated": "[ISO timestamp]",
  "currentPhase": "[phase if changed]",
  "recentActivity": [
    {
      "date": "[date]",
      "type": "[meeting/milestone/update]",
      "summary": "[what happened]"
    }
  ],
  "openIssues": [...],
  "completedIssues": [...],
  "blockers": [...],
  "nextSteps": [...],
  "actionItems": {
    "pending": [...],
    "completed": [...]
  }
}
```

### Step 5: Confirm

```
Updated context for [Project]:

PROJECT_CONTEXT.md:
  - Added entry for [date]

project-state.json:
  - lastUpdated: [timestamp]
  - recentActivity: +1 entry
  - completedIssues: +[n] items
  - openIssues: [n] items
```

---

## When to Use

- After processing a meeting
- After completing significant tasks
- Before generating weekly updates
- When major decisions are made
- At session end

---

## File Locations

Context files typically in project folder:
```
[project-folder]/
├── PROJECT_CONTEXT.md
└── project-state.json
```

---

## Related Skills

- `process-client-meeting` - Calls this after processing
- `create-weekly-update` - Uses context for reports
- `close-session` - May trigger context update
