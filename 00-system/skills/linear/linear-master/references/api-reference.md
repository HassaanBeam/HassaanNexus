# Linear API Reference

## Endpoint

```
POST https://api.linear.app/graphql
```

All operations use this single GraphQL endpoint.

---

## Common Queries

### Get Viewer Info

```graphql
query {
  viewer {
    id
    name
    email
  }
}
```

### List Issues by Project

```graphql
query IssuesByProject($projectName: String!) {
  issues(filter: {
    project: { name: { eq: $projectName } }
  }) {
    nodes {
      id
      identifier
      title
      state { name }
      assignee { name }
      priority
      description
      createdAt
      updatedAt
    }
  }
}
```

### List Issues by State

```graphql
query OpenIssues($projectName: String!) {
  issues(filter: {
    project: { name: { eq: $projectName } },
    state: { name: { in: ["Todo", "In Progress", "In Review"] } }
  }) {
    nodes {
      id
      identifier
      title
      state { name }
      assignee { name }
      priority
    }
  }
}
```

### List Issues Updated Recently

```graphql
query RecentIssues($since: DateTime!) {
  issues(filter: {
    updatedAt: { gt: $since }
  }) {
    nodes {
      id
      identifier
      title
      state { name }
      updatedAt
    }
  }
}
```

### Get Issue Details

```graphql
query GetIssue($id: String!) {
  issue(id: $id) {
    id
    identifier
    title
    description
    state { id name }
    project { id name }
    assignee { id name }
    priority
    labels { nodes { name } }
    comments { nodes { body createdAt user { name } } }
  }
}
```

---

## Common Mutations

### Create Issue

```graphql
mutation CreateIssue($input: IssueCreateInput!) {
  issueCreate(input: $input) {
    success
    issue {
      id
      identifier
      title
      state { name }
    }
  }
}
```

**Variables:**
```json
{
  "input": {
    "title": "Issue title",
    "description": "Issue description",
    "teamId": "team-uuid",
    "projectId": "project-uuid",
    "priority": 2,
    "stateId": "state-uuid"
  }
}
```

### Update Issue

```graphql
mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
  issueUpdate(id: $id, input: $input) {
    success
    issue {
      id
      identifier
      title
      state { name }
    }
  }
}
```

**Variables (change state):**
```json
{
  "id": "issue-uuid",
  "input": {
    "stateId": "new-state-uuid"
  }
}
```

### Add Comment

```graphql
mutation AddComment($issueId: String!, $body: String!) {
  commentCreate(input: {
    issueId: $issueId,
    body: $body
  }) {
    success
    comment {
      id
      body
    }
  }
}
```

---

## Priority Values

| Value | Meaning |
|-------|---------|
| 0 | No priority |
| 1 | Urgent |
| 2 | High |
| 3 | Medium |
| 4 | Low |

---

## Pagination

Linear uses cursor-based pagination:

```graphql
query PaginatedIssues($cursor: String) {
  issues(first: 50, after: $cursor) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      id
      title
    }
  }
}
```

---

## Rate Limits

- 400 requests per minute per API key
- Complex queries count more against limit
- Use `X-RateLimit-*` headers to monitor usage
