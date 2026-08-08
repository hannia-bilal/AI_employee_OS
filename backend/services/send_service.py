"""
Send Email Service
------------------
Handles email sending operations.

Current Behaviour:
- Uses Gmail API when credentials are available.
- Falls back to simulation if Gmail is not configured.
"""

from tools.base_tool import ToolResult, ToolStatus
from utils.simulation_utils import simulation_result


class SendEmailService:

    async def execute(self, params: dict) -> ToolResult:

        recipient = params["to"]
        subject = params["subject"]
        body = params["body"]

        try:

            from services.gmail_service import GmailService

            gmail = GmailService()

            gmail_message_id = await gmail.send_email(
                recipient=recipient,
                subject=subject,
                body=body,
            )

            return ToolResult(
                success=True,
                message=f"✅ Email sent to {recipient}",
                data={
                    "mode": "production",
                    "gmail_configured": True,
                    "gmail_message_id": gmail_message_id,
                    "to": recipient,
                    "subject": subject,
                    "body": body,
                    "status": "sent",
                },
                status=ToolStatus.SUCCESS,
                display_type="card",
            )

        except FileNotFoundError:

            return simulation_result(
                reason="Google OAuth credentials not found (credentials.json).",
                recipient=recipient,
                subject=subject,
                body=body,
            )

        except PermissionError:

            return simulation_result(
                reason="OAuth authorization has not been completed (token.json missing).",
                recipient=recipient,
                subject=subject,
                body=body,
            )

        except RuntimeError as e:

            return simulation_result(
                reason=str(e),
                recipient=recipient,
                subject=subject,
                body=body,
            )

        except Exception as e:

            return ToolResult(
                success=False,
                message="Failed to send email.",
                data={
                    "mode": "error",
                    "error": str(e),
                },
                status=ToolStatus.ERROR,
            )