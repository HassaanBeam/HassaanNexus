---
name: linear-create-tickets
description: Create Linear tickets from action items or task lists. Load when user says "create linear tickets", "add tickets to linear", "create tickets from meeting", "linear ticket for [task]", or wants to convert action items into Linear issues. Supports batch creation with project assignment.
---

# Linear Create Tickets

Create Linear tickets from action items using GraphQL API.

## Configuration

**API Endpoint**: `https://api.linear.app/graphql`
**Auth Header**: `Authorization: {API_KEY}` (no "Bearer" prefix)

---

## Workflow

### Step 1: Get Action Items

Accept from:
1. Output of `create-meeting-minutes`
2. User-provided list
3. Direct input

### Step 2: Filter Items

**Include**:
- Tasks with specific deliverables
- Technical implementation tasks
- Research or documentation tasks

**Exclude**:
- Scheduling tasks ("set up meeting")
- External/client-owned tasks
- Vague items

### Step 3: Get Project Info

Ask user or infer:
- Team name (e.g., "Clients", "Engineering")
- Project name (e.g., "Smartly", "Internal")

### Step 4: Create Tickets

**GraphQL Mutation**:
```graphql
mutation {
  issueCreate(input: {
    title: "Task title",
    teamId: "TEAM_ID",
    projectId: "PROJECT_ID",
    priority: 3,
    description: "## Context\n...\n\n## Description\n..."
  }) {
    success
    issue {
      id
      identifier
      title
      url
    }
  }
}
```

**Priority Values**:
| Priority | Value |
|----------|-------|
| Urgent | 1 |
| High | 2 |
| Medium | 3 |
| Low | 4 |

### Step 5: Report Results

```
Created {count} tickets:

1. CLI-456 - Task title
   URL: https://linear.app/...

2. CLI-457 - Task title
   URL: https://linear.app/...
```

---

## Ticket Format

**Title**: Clear, actionable (no project prefix)
- Good: "Implement data validation"
- Bad: "[Project] Implement validation"

**Description Template**:
```markdown
## Context
[Reference to source - meeting, discussion, etc.]

## Description
[What needs to be done]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

---

## Useful Queries

**Get Teams**:
```graphql
query { teams { nodes { id name } } }
```

**Get Projects in Team**:
```graphql
query($teamId: String!) {
  team(id: $teamId) {
    projects { nodes { id name } }
  }
}
```

---

## Related Skills

- `create-meeting-minutes` - Source of action items
- `linear-update-tickets` - Update existing tickets
- `create-weekly-update` - Uses Linear data
