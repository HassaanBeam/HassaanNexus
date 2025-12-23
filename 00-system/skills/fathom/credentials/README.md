# Fathom Credentials Setup

## Getting Your API Key

1. Log in to [Fathom](https://fathom.video)
2. Go to **Settings** (gear icon)
3. Navigate to **API** section
4. Click **Generate API Key**
5. Copy the key immediately - it won't be shown again

## Configuration

Add to your `.env` file (in Nexus project root):

```bash
FATHOM_API_KEY=your-api-key-here
```

## Verify Setup

```bash
python 00-system/skills/fathom/fathom-master/scripts/fathom_client.py
```

Expected output:
```
Fathom client initialized successfully
Found X meetings
```

## Security

- API key gives full read access to your Fathom account
- Never commit `.env` to git (already in `.gitignore`)
- Rotate key in Fathom settings if compromised

## Troubleshooting

| Issue | Solution |
|-------|----------|
| 401 Unauthorized | Check key is correct, no extra spaces |
| 403 Forbidden | API access may be disabled on your plan |
| Connection error | Check internet, try again |
