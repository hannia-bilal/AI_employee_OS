"""
AI Employee OS - Email Tool (Stub)
Module Owner: Taskeen Mustafa
Status: STUB — Replace with real implementation

This stub simulates email operations so the AI agent
can be tested end-to-end before the real module is ready.

HOW TO REPLACE:
  1. Keep the same file name: email_tool.py
  2. Keep the same class names: DraftEmailTool, SendEmailTool, SummarizeEmailTool
  3. Keep the same .name property values: "draft_email", "send_email", "summarize_email"
  4. Implement real logic in execute() — just return a ToolResult
  5. Remove is_mock from the data dict
  6. Drop this file into tools/ and restart the server
"""
from datetime import datetime

from tools.base_tool import BaseTool, ToolResult, ToolParameter, ToolStatus
from services.draft_service import DraftEmailService

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
        valid, message = self.validate_params(params)

        if not valid:
            return ToolResult(
                success=False,
                message=message,
                status=ToolStatus.ERROR,
            )

        service = DraftEmailService()
        return await service.execute(params)


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
        to = params.get("to", "taskeen.mustafa@codecelix.com")
        subject = params.get("subject", "No Subject")

        return ToolResult(
            success=True,
            message=f'✅ Email sent to {to}: "{subject}"',
            data={
                "is_mock": True,
                "email_id": f"EMAIL-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "to": to,
                "subject": subject,
                "body": params.get("body", ""),
                "status": "sent",
                "sent_at": datetime.now().isoformat(),
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
        return ToolResult(
            success=True,
            message="📋 Email summary generated",
            data={
                "is_mock": True,
                "summary": "Meeting scheduled for Friday after Jummah to discuss Project 3 AI Agent. Action items: Muhammad Awais to integrate AI brain, Faez to finish CRM.",
                "key_points": [
                    "Meeting confirmed for Friday post-Jummah",
                    "Project 3 AI Agent discussion",
                    "AI brain integration needed",
                ],
                "action_items": [
                    "Awais to integrate AI brain",
                    "Faez to update CRM module",
                ],
            },
            display_type="card",
        )
