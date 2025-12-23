# Fathom Authentication

## Overview

Fathom uses API key authentication via the `X-Api-Key` header.

---

## Getting Your API Key

1. Log in to [Fathom](https://fathom.video)
2. Go to **Settings** (gear icon)
3. Navigate to **API** section
4. Click **Generate API Key**
5. Copy the key immediately - it won't be shown again

---

## Environment Configuration

Add to your `.env` file (at Nexus project root):

```
FATHOM_API_KEY=your-api-key-here
```

---

## Using the Key

Include in all API requests as `X-Api-Key` header:

```python
headers = {
    "X-Api-Key": api_key,
    "Content-Type": "application/json"
}
```

**Example cURL:**
```bash
curl -s --request GET \
  --url 'https://api.fathom.ai/external/v1/meetings' \
  --header 'X-Api-Key: YOUR_API_KEY'
```

---

## Key Properties

- **Expiration**: Keys do not expire automatically
- **Rotation**: Generate a new key in settings to rotate
- **Revocation**: Delete the key in settings to revoke

---

## Security Best Practices

- Never commit API keys to git
- Use environment variables (`.env` is gitignored)
- Rotate key if compromised
- Use one key per integration/application

---

## Troubleshooting

### 401 Unauthorized
- API key is invalid or revoked
- Check key is correct in `.env`
- Verify header name is `X-Api-Key` (not `Authorization`)

### 403 Forbidden
- API access may be disabled on your account
- Contact Fathom support

---

## References

- [Fathom API Documentation](https://fathom.video/api)
