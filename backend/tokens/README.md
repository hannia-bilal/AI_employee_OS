# Gmail OAuth Tokens

This directory stores OAuth tokens generated after the first successful Gmail authentication.

## Files

### token.json
Generated automatically by the application after completing OAuth authentication.

**Do not commit this file to Git.**

### token.example.json
Example structure showing the expected token format.
Replace placeholder values only if you need to inspect the structure.

## First-time Setup

1. The project owner places `credentials.json` in `backend/auth/`.
2. Run the application.
3. Complete the Google OAuth login.
4. The application automatically creates `token.json` in this directory.