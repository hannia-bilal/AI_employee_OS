"""
AI Employee OS - Email Tool
Real implementation backed by the database.
"""
from tools.base_tool import BaseTool, ToolResult, ToolParameter, ToolStatus
from services.draft_service import DraftEmailService
from services.send_service import SendEmailService
from services.summarize_service import SummarizeEmailService



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

        valid, message = self.validate_params(params)

        if not valid:
            return ToolResult(
                success=False,
                message=message,
                status=ToolStatus.ERROR,
            )

        service = SendEmailService()
        return await service.execute(params)


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
            ToolParameter(
                "email_content",
                "string",
                "Email content to summarize",
            ),
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

        service = SummarizeEmailService()

        return await service.execute(params)
