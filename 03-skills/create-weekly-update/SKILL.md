---
name: create-weekly-update
description: Generate weekly status update based on Linear ticket activity and project progress. Load when user says "weekly update", "weekly status", "create weekly report", "status update for [project]", "what got done this week". Fetches ticket changes and generates formatted summary.
---

# Create Weekly Update

Generate weekly status update from Linear activity.

## Workflow

### Step 1: Identify Scope

Ask if not clear:
- Project name in Linear
- Team name
- Time period (default: 7 days)

### Step 2: Fetch Ticket Changes

**Query tickets updated in period**:
```graphql
query($teamId: String!, $updatedAfter: DateTime!) {
  team(id: $teamId) {
    projects {
      nodes {
        name
        issues(filter: { updatedAt: { gte: $updatedAfter } }) {
          nodes {
            identifier
            title
            state { name }
            completedAt
            updatedAt
          }
        }
      }
    }
  }
}
```

### Step 3: Categorize Tickets

**Done This Period**:
- Tickets marked Done with completedAt in range

**In Progress**:
- Tickets in "In Progress" or "In Review" state

**To Do**:
- Tickets in "Todo" state

### Step 4: Display Current State

```
📊 Status for [Project] (Last 7 Days)

✅ Completed (3):
- CLI-400: Data pipeline setup
- CLI-401: Integration testing
- CLI-402: Documentation

🔄 In Progress (2):
- CLI-456: Validation implementation
- CLI-457: API integration

📋 Todo (4):
- CLI-458: Architecture review
- CLI-459: Performance testing
- CLI-460: UAT
- CLI-461: Deployment
```

### Step 5: Ask for Updates (Optional)

```
Would you like to update any tickets?
1. Update status (e.g., move CLI-456 to Done)
2. Continue without changes
```

If updates requested, use `linear-update-tickets`.

### Step 6: Generate Summary

**Weekly Update Format**:
```markdown
# [Project] Weekly Update - [Date]

## Done Last Week
- [Description] - CLI-XXXX
- [Description] - CLI-XXXX

## To be Done This Week
- [Description] - CLI-XXXX
- [Description] - CLI-XXXX
```

**Format Rules**:
- NO project prefixes in titles
- 1-line descriptions only
- Always include ticket numbers (CLI-XXXX)

### Step 7: Save/Share

Options:
- Save to file: `[folder]/weekly-updates/YYYY-MM-DD-Update.md`
- Post to Slack
- Copy to clipboard

---

## Output

```json
{
  "project": "Project Name",
  "period": "2025-12-09 to 2025-12-15",
  "completed": [...],
  "in_progress": [...],
  "todo": [...],
  "summary_markdown": "..."
}
```

---

## Related Skills

- `linear-update-tickets` - Update ticket status
- `update-project-context` - Sync after generating
- `send-internal-update` - Share with team
