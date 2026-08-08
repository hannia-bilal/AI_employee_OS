"""
Gmail Authentication
--------------------
Handles OAuth authentication for the Gmail API.

Expected files:

backend/auth/credentials.json
backend/tokens/token.json
"""

from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from config import settings


class GmailAuth:
    """Handles Gmail OAuth authentication."""

    def __init__(self):

        self.base_dir = Path(__file__).resolve().parent.parent

        self.credentials_path = (
            self.base_dir / "auth" / "credentials.json"
        )

        self.token_path = (
            self.base_dir / "tokens" / "token.json"
        )

        self.scopes = settings.GMAIL_SCOPES.split()

        # Ensure token directory exists
        self.token_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def get_credentials(self) -> Credentials:
        """
        Returns valid Gmail OAuth credentials.

        Behaviour:
        - Uses existing token if available.
        - Refreshes expired tokens.
        - Starts OAuth flow if no valid token exists.
        """

        creds = None

        # --------------------------------------------------
        # Load existing OAuth token
        # --------------------------------------------------

        if self.token_path.exists():

            try:

                creds = Credentials.from_authorized_user_file(
                    str(self.token_path),
                    self.scopes,
                )

            except Exception:

                # Corrupted token
                self.token_path.unlink(missing_ok=True)

                creds = None

        # --------------------------------------------------
        # Refresh expired token
        # --------------------------------------------------

        if (
            creds
            and creds.expired
            and creds.refresh_token
        ):

            try:

                creds.refresh(Request())

                with open(
                    self.token_path,
                    "w",
                    encoding="utf-8",
                ) as token:

                    token.write(
                        creds.to_json()
                    )

                return creds

            except Exception:

                # Refresh failed.
                # Remove old token and perform OAuth again.
                self.token_path.unlink(
                    missing_ok=True
                )

                creds = None

        # --------------------------------------------------
        # OAuth Authorization
        # --------------------------------------------------

        if not creds or not creds.valid:

            if not self.credentials_path.exists():

                raise FileNotFoundError(
                    "\n"
                    "Google OAuth credentials not found.\n\n"
                    "Expected location:\n"
                    "backend/auth/credentials.json\n\n"
                    "Copy:\n"
                    "backend/auth/credentials.example.json\n"
                    "to credentials.json and replace the placeholders."
                )

            try:

                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_path),
                    self.scopes,
                )

                creds = flow.run_local_server(
                    port=0
                )

                with open(
                    self.token_path,
                    "w",
                    encoding="utf-8",
                ) as token:

                    token.write(
                        creds.to_json()
                    )

            except Exception as e:

                raise RuntimeError(
                    f"Gmail OAuth authorization failed: {e}"
                )

        return creds