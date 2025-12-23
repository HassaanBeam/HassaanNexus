---
name: fathom-connect
description: Set up Fathom API connection. Load when user says "connect fathom", "setup fathom", "configure fathom api", or needs to authenticate with Fathom for the first time.
version: "1.0"
---

# Fathom Connect

Set up and verify Fathom API connection.

## Purpose

Guides user through Fathom API setup:
1. Get API key from Fathom
2. Configure in `.env`
3. Verify connection works

## Workflow

### Step 1: Check Current Status

```bash
python 00-system/skills/fathom/fathom-master/scripts/fathom_client.py
```

**If configured:**
```
Fathom client initialized successfully
Found X meetings
```

**If not configured:**
```
Configuration error: FATHOM_API_KEY not found in .env or environment
```

### Step 2: Get API Key (if needed)

1. Go to [fathom.video](https://fathom.video)
2. Click Settings (gear icon)
3. Navigate to API section
4. Click "Generate API Key"
5. Copy the key

### Step 3: Configure

Add to `.env` file:
```bash
FATHOM_API_KEY=your-key-here
```

### Step 4: Verify

```bash
python 00-system/skills/fathom/fathom-master/scripts/fathom_client.py
```

### Step 5: Confirm Success

```
Fathom connection configured!

API Status: Connected
Meetings accessible: Yes

You can now use:
- "fetch meetings for [client]"
- "get transcript for [meeting]"
- "process meeting" workflow
```

## Troubleshooting

| Error | Solution |
|-------|----------|
| FATHOM_API_KEY not found | Add key to .env file |
| 401 Unauthorized | Key is invalid - regenerate in Fathom |
| 403 Forbidden | API not enabled on your Fathom plan |

---

**Version**: 1.0
