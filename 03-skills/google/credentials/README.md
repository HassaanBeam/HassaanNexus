# Google Credentials Setup

This folder contains credential templates for Google OAuth integration.

## Setup Instructions

1. **Copy the example file:**
   ```bash
   cp google-credentials.example.json google-credentials.json
   ```

2. **Get your credentials from Google Cloud Console:**
   - Go to https://console.cloud.google.com/
   - Navigate to APIs & Services → Credentials
   - Create OAuth 2.0 Client ID (Desktop App type)
   - Download the JSON

3. **Either:**
   - Replace `google-credentials.json` with your downloaded file, OR
   - Add to your `.env` file:
     ```
     GOOGLE_CLIENT_ID=your-client-id
     GOOGLE_CLIENT_SECRET=your-client-secret
     GOOGLE_PROJECT_ID=your-project-id
     ```

## Security

- `google-credentials.json` is gitignored - your real credentials won't be committed
- `google-credentials.example.json` is tracked - it's just a template
- Always use `.env` for sensitive values

## Token Storage

After OAuth authorization, tokens are stored in:
- `01-memory/integrations/google-token.json` (also gitignored)
