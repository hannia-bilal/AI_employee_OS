"""
Gmail Utilities
---------------
Helper functions for Gmail API.
"""

import base64


class GmailUtils:

    @staticmethod
    def decode_base64(data: str) -> str:
        """
        Decode Gmail base64url encoded data.
        """
        if not data:
            return ""

        decoded = base64.urlsafe_b64decode(
            data.encode("UTF-8")
        )

        return decoded.decode("utf-8", errors="ignore")

    @staticmethod
    def extract_headers(payload: dict) -> dict:
        """
        Convert Gmail headers into a dictionary.
        """

        headers = {}

        for item in payload.get("headers", []):

            headers[item["name"]] = item["value"]

        return headers

    @staticmethod
    def extract_body(payload: dict) -> str:
        """
        Extract plain text body from Gmail payload.
        """

        body = ""

        if payload.get("body", {}).get("data"):
            return GmailUtils.decode_base64(
                payload["body"]["data"]
            )

        for part in payload.get("parts", []):

            mime_type = part.get("mimeType")

            if mime_type == "text/plain":

                data = part.get("body", {}).get("data")

                if data:
                    body += GmailUtils.decode_base64(data)

        return body

    @staticmethod
    def parse_message(message: dict) -> dict:
        """
        Convert Gmail message into a simplified structure.
        """

        payload = message.get("payload", {})

        headers = GmailUtils.extract_headers(payload)

        return {
            "id": message.get("id"),
            "thread_id": message.get("threadId"),
            "label_ids": message.get("labelIds", []),
            "snippet": message.get("snippet"),
            "subject": headers.get("Subject"),
            "from": headers.get("From"),
            "to": headers.get("To"),
            "date": headers.get("Date"),
            "body": GmailUtils.extract_body(payload),
        }

    def simulation_result(reason, recipient, subject, body):
        return ToolResult(
            success=True,
            message="📧 Simulation mode active.",
            data={
                "mode": "simulation",
                "reason": reason,
                "to": recipient,
                "subject": subject,
                "body": body,
                "status": "simulated",
            },
            status=ToolStatus.SUCCESS,
            display_type="card",
        )