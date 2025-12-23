---
name: linear-update-tickets
description: Update Linear ticket status or add comments. Load when user says "update linear ticket", "mark ticket as done", "move CLI-XXX to [status]", "change ticket status", "add comment to ticket", or "close ticket". Supports state changes and comments.
---

# Linear Update Tickets

Update Linear ticket status or add comments.

## Configuration

**API Endpoint**: `https://api.linear.app/graphql`
**Auth Header**: `Authorization: {API_KEY}`

---

## Workflow

### Step 1: Identify Ticket

Get ticket identifier:
- From user: "CLI-123" or "update ticket CLI-123"
- From context: Referenced in discussion

### Step 2: Determine Update

Options:
- **Status change**: Todo → In Progress → In Review → Done
- **Add comment**: Context or update note
- **Both**: Change status with comment

### Step 3: Execute Update

**Update Status**:
```graphql
mutation {
  issueUpdate(
    id: "ISSUE_ID",
    input: { stateId: "STATE_ID" }
  ) {
    success
    issue {
      identifier
      title
      state { name }
    }
  }
}
```

**Add Comment**:
```graphql
mutation {
  commentCreate(input: {
    issueId: "ISSUE_ID",
    body: "Comment text"
  }) {
    success
    comment { id body }
  }
}
```

### Step 4: Confirm

```
Updated CLI-123:
  - Status: In Progress → Done
  - Comment added: "Completed per discussion"
```

---

## Common State IDs

State IDs vary by team. Query to get them:
```graphql
query($teamId: String!) {
  team(id: $teamId) {
    states { nodes { id name } }
  }
}
```

**Example (Clients team)**:
| State | ID |
|-------|-----|
| Todo | `d8899534-...` |
| In Progress | `9a2c9ba8-...` |
| In Review | `7866c5ad-...` |
| Done | `40112a2a-...` |

---

## Batch Updates

For multiple tickets:
```
Update tickets CLI-123, CLI-124, CLI-125 to Done
```

Process each sequentially and report results.

---

## Related Skills

- `linear-create-tickets` - Create new tickets
- `create-weekly-update` - Report on ticket changes
- `process-client-meeting` - May update tickets from discussion
