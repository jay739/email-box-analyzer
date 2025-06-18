# Gmail OAuth2 Setup Guide

This guide will help you set up Gmail OAuth2 authentication for the Email Box Analyzer.

## Prerequisites

- A Google account
- Access to Google Cloud Console

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter a project name (e.g., "Email Box Analyzer")
4. Click "Create"

## Step 2: Enable Gmail API

1. In your project, go to "APIs & Services" → "Library"
2. Search for "Gmail API"
3. Click on "Gmail API"
4. Click "Enable"

## Step 3: Create OAuth2 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - **User Type**: External
   - **App name**: Email Box Analyzer
   - **User support email**: Your email
   - **Developer contact information**: Your email
   - **Scopes**: Add `https://www.googleapis.com/auth/gmail.readonly`
4. Click "Save and Continue" through the remaining steps
5. Back to "Create OAuth client ID":
   - **Application type**: Desktop application
   - **Name**: Email Box Analyzer Desktop
6. Click "Create"
7. Download the JSON file (rename it to `credentials.json`)

## Step 4: Install Credentials

1. Create the OAuth directory:
   ```bash
   mkdir -p ~/.email_analyzer/oauth
   ```

2. Move the downloaded credentials:
   ```bash
   mv ~/Downloads/credentials.json ~/.email_analyzer/oauth/
   ```

## Step 5: Test the Setup

1. Start your backend:
   ```bash
   make run
   ```

2. Visit the API documentation:
   ```
   http://localhost:8000/docs
   ```

3. Test the OAuth2 endpoints:
   - `POST /api/oauth/gmail/auth` - Start authentication
   - `GET /api/oauth/gmail/status` - Check status

## OAuth2 Flow

### 1. Start Authentication
```bash
curl -X POST "http://localhost:8000/api/oauth/gmail/auth" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

Response:
```json
{
  "success": true,
  "message": "Please visit the authorization URL",
  "auth_url": "https://accounts.google.com/oauth/authorize?...",
  "user_info": null
}
```

### 2. User Authorization
1. Open the `auth_url` in your browser
2. Sign in with your Google account
3. Grant permissions to the app
4. Copy the authorization code from the redirect URL

### 3. Complete Authentication
```bash
curl -X POST "http://localhost:8000/api/oauth/gmail/callback" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"authorization_code": "YOUR_AUTH_CODE"}'
```

### 4. Use Gmail API
Once authenticated, you can:
- Get labels: `GET /api/oauth/gmail/labels`
- Get messages: `GET /api/oauth/gmail/messages`
- Get stats: `GET /api/oauth/gmail/stats`

## Security Notes

- Keep `credentials.json` secure and never commit it to version control
- The app will store tokens in `~/.email_analyzer/oauth/token.pickle`
- Tokens are automatically refreshed when needed
- You can revoke access anytime in your Google Account settings

## Troubleshooting

### "OAuth2 credentials not found"
- Ensure `credentials.json` is in `~/.email_analyzer/oauth/`
- Check file permissions

### "Invalid client" error
- Verify the credentials file is correct
- Check that the OAuth consent screen is configured

### "Access denied" error
- Make sure you've granted the necessary permissions
- Check that the Gmail API is enabled

### Token refresh issues
- Delete `~/.email_analyzer/oauth/token.pickle` to force re-authentication
- Check that your Google account has 2FA enabled

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/oauth/gmail/auth` | POST | Start OAuth2 flow |
| `/api/oauth/gmail/callback` | POST | Complete OAuth2 flow |
| `/api/oauth/gmail/status` | GET | Check authentication status |
| `/api/oauth/gmail/disconnect` | POST | Disconnect OAuth2 session |
| `/api/oauth/gmail/labels` | GET | Get Gmail labels |
| `/api/oauth/gmail/messages` | GET | Get Gmail messages |
| `/api/oauth/gmail/stats` | GET | Get Gmail statistics |

## Next Steps

1. Integrate OAuth2 flow into your frontend
2. Handle token refresh automatically
3. Add support for other email providers (Outlook, Yahoo)
4. Implement proper session management for multiple users 