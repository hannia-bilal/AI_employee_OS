"""
Gmail Service
-------------
Provides Gmail API operations.

Must do:
- Place credentials.json in backend/auth/
- Complete OAuth authorization once.
"""

import base64
from email.mime.text import MIMEText

from googleapiclient.discovery import build

from auth.gmail_auth import GmailAuth
from utils.gmail_utils import GmailUtils


class GmailService:
    """Service class for interacting with the Gmail API."""

    def __init__(self):
        auth = GmailAuth()
        credentials = auth.get_credentials()

        self.service = build(
            "gmail",
            "v1",
            credentials=credentials,
        )

    async def send_email(
        self,
        recipient: str,
        subject: str,
        body: str,
    ) -> str:
        """
        Send an email using Gmail API.

        Returns:
            Gmail Message ID.
        """
        try:
            message = MIMEText(body)

            message["to"] = recipient
            message["subject"] = subject

            raw = base64.urlsafe_b64encode(
                message.as_bytes()
            ).decode()

            sent_message = (
                self.service.users()
                .messages()
                .send(
                    userId="me",
                    body={"raw": raw},
                )
                .execute()
            )

            return sent_message["id"]

        except Exception as e:
            raise Exception(f"Gmail API Error while sending email: {e}")

    async def get_email(
        self,
        email_id: str,
    ) -> dict:
        """
        Retrieve and parse a single Gmail message.
        """
        try:
            message = (
                self.service.users()
                .messages()
                .get(
                    userId="me",
                    id=email_id,
                    format="full",
                )
                .execute()
            )

            return GmailUtils.parse_message(message)

        except Exception as e:
            raise Exception(f"Gmail API Error while retrieving email: {e}")

    async def list_emails(
        self,
        query: str = "",
        max_results: int = 10,
    ) -> list:
        """
        Retrieve a list of parsed emails.
        """
        try:
            response = (
                self.service.users()
                .messages()
                .list(
                    userId="me",
                    q=query,
                    maxResults=max_results,
                )
                .execute()
            )

            emails = []

            for item in response.get("messages", []):
                emails.append(
                    await self.get_email(item["id"])
                )

            return emails

        except Exception as e:
            raise Exception(f"Gmail API Error while listing emails: {e}")

    async def get_thread(
        self,
        thread_id: str,
    ) -> list:
        """
        Retrieve an email thread and return parsed messages.
        """
        try:
            thread = (
                self.service.users()
                .threads()
                .get(
                    userId="me",
                    id=thread_id,
                )
                .execute()
            )

            return [
                GmailUtils.parse_message(message)
                for message in thread.get("messages", [])
            ]

        except Exception as e:
            raise Exception(f"Gmail API Error while retrieving thread: {e}")

    async def delete_email(
        self,
        email_id: str,
    ) -> bool:
        """
        Delete an email.

        Returns:
            True if deletion succeeds.
        """
        try:
            self.service.users().messages().delete(
                userId="me",
                id=email_id,
            ).execute()

            return True

        except Exception as e:
            raise Exception(f"Gmail API Error while deleting email: {e}")