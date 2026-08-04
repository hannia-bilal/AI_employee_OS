"""
Gmail Service
-------------
Handles Gmail authentication and API communication.
"""


class GmailService:

    def __init__(self):
        pass

    async def send_email(
        self,
        recipient: str,
        subject: str,
        body: str,
    ):
        """
        TODO

        Authenticate user.

        Build MIME message.

        Send through Gmail API.

        Return Gmail Message ID.
        """
        raise NotImplementedError(
            "Gmail integration not implemented yet."
        )

    async def read_email(
        self,
        email_id: str,
    ):
        """
        TODO

        Retrieve email body.

        Used by Summary Service.
        """
        raise NotImplementedError(
            "Gmail integration not implemented yet."
        )