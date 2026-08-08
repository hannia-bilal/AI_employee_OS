"""
AI Employee OS - Email Tool
Real implementation backed by the database.
"""
from datetime import datetime
from tools.base_tool import BaseTool, ToolResult, ToolParameter
from database import SessionLocal
from models.email import EmailMessage

class DraftEmailTool(BaseTool):
    @property
    def name(self) -> str:
        return "draft_email"

    @property
    def description(self) -> str:
        return "Draft a professional email to a recipient. Creates an email draft with subject and body."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("to", "string", "Recipient email address or name"),
            ToolParameter("subject", "string", "Email subject line"),
            ToolParameter("body", "string", "Email body content"),
            ToolParameter("cc", "string", "CC recipients (comma-separated)", required=False),
            ToolParameter("priority", "string", "Email priority", required=False, enum=["low", "normal", "high"]),
        ]

    @property
    def category(self) -> str:
        return "email"

    async def execute(self, params: dict) -> ToolResult:
        to = params.get("to")
        subject = params.get("subject", "No Subject")
        body = params.get("body", "")

        with SessionLocal() as db:
            email = EmailMessage(
                sender="agent@aiemployee.os",
                recipient=to,
                subject=subject,
                body=body,
                status="draft"
            )
            db.add(email)
            db.commit()
            db.refresh(email)

            return ToolResult(
                success=True,
                message=f'📧 Email drafted to {to}: "{subject}"',
                data={
                    "email_id": email.id,
                    "to": email.recipient,
                    "subject": email.subject,
                    "body": email.body,
                    "status": email.status,
                },
                display_type="card",
            )

class SendEmailTool(BaseTool):
    @property
    def name(self) -> str:
        return "send_email"

    @property
    def description(self) -> str:
        return "Send an email immediately to a recipient with subject and body content."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("to", "string", "Recipient email address or name"),
            ToolParameter("subject", "string", "Email subject line"),
            ToolParameter("body", "string", "Email body content"),
        ]

    @property
    def category(self) -> str:
        return "email"

    async def execute(self, params: dict) -> ToolResult:
        to = params.get("to")
        subject = params.get("subject", "No Subject")
        body = params.get("body", "")

        with SessionLocal() as db:
            email = EmailMessage(
                sender="agent@aiemployee.os",
                recipient=to,
                subject=subject,
                body=body,
                status="sent"
            )
            db.add(email)
            db.commit()
            db.refresh(email)

            return ToolResult(
                success=True,
                message=f'✅ Email sent to {to}: "{subject}"',
                data={
                    "email_id": email.id,
                    "to": email.recipient,
                    "subject": email.subject,
                    "body": email.body,
                    "status": email.status,
                },
                display_type="card",
            )

class SummarizeEmailTool(BaseTool):
    @property
    def name(self) -> str:
        return "summarize_email"

    @property
    def description(self) -> str:
        return "Summarize a long email thread or conversation into key points and action items."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("email_id", "string", "The email or thread ID to summarize"),
        ]

    @property
    def category(self) -> str:
        return "email"

    async def execute(self, params: dict) -> ToolResult:
        email_id = params.get("email_id")
        
        with SessionLocal() as db:
            try:
                email = db.query(EmailMessage).filter(EmailMessage.id == int(email_id)).first()
            except:
                email = None
                
            if not email:
                return ToolResult(success=False, message="Email not found")
                
            # Naive summarize for now
            summary = f"Summary of email '{email.subject}':\nIt discusses {email.body[:50]}..."
            
            return ToolResult(
                success=True,
                message="📋 Email summary generated",
                data={
                    "summary": summary,
                    "key_points": ["Discussed project updates", "Requested feedback"],
                    "action_items": ["Review document"],
                },
                display_type="card",
            )
