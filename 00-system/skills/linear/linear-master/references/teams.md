# Linear Teams Reference

## Clients Team

**Team ID**: `2686694f-6343-48a0-9efb-d69d77aaa621`

### State IDs

| State | ID |
|-------|-----|
| Todo | `d8899534-a204-4446-a06b-681cbc4c6e04` |
| In Progress | `9a2c9ba8-5931-491e-8298-c9fb761aab23` |
| In Review | `7866c5ad-5654-4516-849f-b3f7462613d6` |
| Done | `40112a2a-870e-48ca-aeff-7f16356acd90` |

---

## Known Projects

| Project | Client |
|---------|--------|
| Moverii | Moverii |
| Doula Givers | Doula Givers |
| Rivertrace | Rivertrace |
| Smartly | Smartly |

---

## Querying Team Info

To get fresh team/state IDs:

```graphql
query {
  teams {
    nodes {
      id
      name
      states {
        nodes {
          id
          name
          type
        }
      }
    }
  }
}
```

---

## Querying Projects

```graphql
query {
  projects {
    nodes {
      id
      name
      state
    }
  }
}
```
