# Slack Credentials Setup

Credentials are **included** - you just need to authorize your account.

## Quick Start (30 seconds)

### Step 1: Add Credentials to .env

Copy these lines to your `.env` file (in project root):

```bash
# Slack App Credentials (shared - identifies the app)
SLACK_CLIENT_ID=3499735674373.10122697240033
SLACK_CLIENT_SECRET=dce1a170a489edab7234411850b8aeab
```

Or copy from `slack-credentials.json` in this folder.

### Step 2: Authorize Your Account

```bash
python 00-system/skills/slack/slack-master/scripts/setup_slack.py
```

Browser opens → Sign in to Slack → Click "Allow" → Done!

### Step 3: Verify

```bash
python 00-system/skills/slack/slack-master/scripts/check_slack_config.py
```

You should see:
```
[OK] SLACK_USER_TOKEN configured
[OK] API connection successful
```

**That's it!**

---

## What's in This Folder

| File | Purpose |
|------|---------|
| `slack-credentials.json` | App credentials (Client ID + Secret) - copy to .env |
| `slack-app-manifest.json` | Template to create your own Slack app (optional) |
| `README.md` | This guide |

---

## How It Works

| Component | What It Is | Shared? |
|-----------|-----------|---------|
| Client ID + Secret | Identifies the Slack App | Yes (included) |
| User Token | Your personal authorization | No (you create it) |

- **Client credentials** identify the app - safe to share
- **User token** grants access to YOUR account - never share

---

## Team Deployment

Since credentials are included, each team member just:

1. Copies Client ID/Secret to their `.env`
2. Runs `setup_slack.py` to authorize
3. Gets their own personal token

Messages appear as each individual user.

---

## Creating Your Own App (Optional)

If you want your own Slack App instead of using the shared one:

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click **Create New App** → **From an app manifest**
3. Paste contents of `slack-app-manifest.json`
4. Get your own Client ID/Secret from **Basic Information**
5. Replace the values in your `.env`

---

## Security

### Safe to Share
- Client ID - Public app identifier
- Client Secret - Identifies app, not users
- App Manifest - Template for creating apps

### Never Share
- User Token (`SLACK_USER_TOKEN`) - Grants access to YOUR Slack
- Stored only in your local `.env`
- Already in `.gitignore`
