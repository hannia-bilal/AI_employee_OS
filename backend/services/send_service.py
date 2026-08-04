"""
Send Email Service
------------------
Handles email sending operations.

Current Version:
- Simulates email sending.
- Ready for Gmail API integration.
"""

from datetime import datetime

from tools.base_tool import ToolResult, ToolStatus


class SendEmailService:

    async def execute(self, params: dict) -> ToolResult:
        try:
            recipient = params.get("to")
            subject = params.get("subject")
            body = params.get("body")

            if not recipient:
                return ToolResult(
                    success=False,
                    message="Recipient is required.",
                    status=ToolStatus.ERROR,
                )

            if not subject:
                return ToolResult(
                    success=False,
                    message="Subject is required.",
                    status=ToolStatus.ERROR,
                )

            if not body:
                return ToolResult(
                    success=False,
                    message="Email body is required.",
                    status=ToolStatus.ERROR,
                )

            # =====================================================
            # TODO:
            # Replace this simulation with GmailService.
            #
            # Example:
            #
            # from services.gmail_service import GmailService
            #
            # gmail = GmailService()
            #
            # gmail_message_id = await gmail.send_email(
            #     recipient=recipient,
            #     subject=subject,
            #     body=body,
            # )
            #
            # return ToolResult(
            #     success=True,
            #     message=f'✅ Email sent to {recipient}',
            #     data={
            #         "gmail_message_id": gmail_message_id,
            #         "to": recipient,
            #         "subject": subject,
            #         "body": body,
            #         "status": "sent",
            #     },
            #     status=ToolStatus.SUCCESS,
            #     display_type="card",
            # )
            # =====================================================

            email_id = f"EMAIL-{datetime.now().strftime('%Y%m%d%H%M%S')}"

            return ToolResult(
                success=True,
                message=f'✅ Email sent to {recipient}: "{subject}"',
                data={
                    "email_id": email_id,
                    "to": recipient,
                    "subject": subject,
                    "body": body,
                    "status": "sent",
                    "sent_at": datetime.now().isoformat(),
                },
                status=ToolStatus.SUCCESS,
                display_type="card",
            )

        except Exception as e:
            return ToolResult(
                success=False,
                message="Failed to send email.",
                data={
                    "error": str(e),
                },
                status=ToolStatus.ERROR,
            )