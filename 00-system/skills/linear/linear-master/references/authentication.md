# Linear Authentication

## Overview

Linear uses Personal API Keys for authentication. The key is passed directly in the `Authorization` header (NOT as Bearer token).

---

## Getting Your API Key

1. Log in to [Linear](https://linear.app)
2. Go to **Settings** (gear icon)
3. Navigate to **API** section
4. Click **Create key** under "Personal API keys"
5. Give it a name (e.g., "Nexus Integration")
6. Copy the key - it starts with `lin_api_`

---

## Environment Configuration

Add to your `.env` file (at Nexus project root):

```
LINEAR_API_KEY=lin_api_xxxxxxxxxxxxx
```

---

## Using the Key

**Important**: Linear does NOT use Bearer token format. Pass the key directly:

```python
headers = {
    "Authorization": api_key,  # NOT "Bearer {api_key}"
    "Content-Type": "application/json"
}
```

**Example cURL:**
```bash
curl -X POST https://api.linear.app/graphql \
  -H "Authorization: lin_api_xxxxx" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ viewer { id name } }"}'
```

---

## Key Properties

- **Expiration**: Keys do not expire automatically
- **Scope**: Full access to your workspace
- **Rotation**: Create new key and delete old one to rotate

---

## Security Best Practices

- Never commit API keys to git
- Use environment variables (`.env` is gitignored)
- Rotate key if compromised
- Each team member should use their own key

---

## Troubleshooting

### 401 Unauthorized
- API key is invalid or revoked
- Check key starts with `lin_api_`
- Verify you're NOT using `Bearer` prefix

### 403 Forbidden
- You don't have access to requested resource
- Check you're querying your own workspace

---

## References

- [Linear API Documentation](https://developers.linear.app)
- [GraphQL Playground](https://api.linear.app/graphql) (use with Authorization header)
