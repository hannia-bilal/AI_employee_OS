# Gmail Credentials

Place the Google OAuth credentials file here.

Required filename:

credentials.json

The project owner should download this file from

Google Cloud Console

Credentials → OAuth Client ID

and copy it into this directory.


## Gmail API Setup

1. Enable the Gmail API in Google Cloud Console.
2. Download OAuth client credentials.
3. Copy the file to:
   backend/auth/credentials.json
4. Copy `.env.example` to `.env` and configure your environment variables.
5. Run the application. On the first Gmail operation, complete the OAuth authorization flow. A `token.json` file will be created automatically in `backend/tokens/`.