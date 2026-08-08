"""
Summarize Email Service
-----------------------
Generates concise summaries of email content using Groq LLM.
"""

from tools.base_tool import ToolResult, ToolStatus

from services.llm_service import LLMService
from prompts.summarize_prompt import (
    SYSTEM_PROMPT,
    build_summary_prompt,
)


class SummarizeEmailService:

    def __init__(self):
        self.llm = LLMService()

    async def execute(self, params: dict) -> ToolResult:
        try:

            email_content = params.get("email_content")

            if not email_content:
                return ToolResult(
                    success=False,
                    message="Parameter 'email_content' is required.",
                    status=ToolStatus.ERROR,
                )

            prompt = build_summary_prompt(email_content)

            response = await self.llm.generate(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=prompt,
            )

            summary = response.strip()

            key_points = []

            action_items = []

            for line in summary.splitlines():

                text = line.strip("-• ").strip()

                if not text:
                    continue

                if text.lower().startswith("action"):
                    action_items.append(text)

                else:
                    key_points.append(text)

            return ToolResult(
                success=True,
                message="📋 Email summary generated",
                data={
                    "summary": summary,
                    "key_points": key_points,
                    "action_items": action_items,
                },
                status=ToolStatus.SUCCESS,
                display_type="card",
            )

        except Exception as e:

            return ToolResult(
                success=False,
                message="Failed to summarize email.",
                data={
                    "error": str(e),
                },
                status=ToolStatus.ERROR,
            )