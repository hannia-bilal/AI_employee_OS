"""
Draft Email Service
-------------------
Generates professional email drafts using Groq LLM.
"""

from datetime import datetime

from tools.base_tool import ToolResult, ToolStatus

from services.llm_service import LLMService
from prompts.draft_prompt import (
    SYSTEM_PROMPT,
    build_draft_prompt,
)


class DraftEmailService:

    def __init__(self):
        self.llm = LLMService()

    async def execute(self, params: dict) -> ToolResult:
        try:

            recipient = params.get("to", "")
            subject = params.get("subject", "")
            body = params.get("body", "")
            priority = params.get("priority", "normal")
            cc = params.get("cc")

            # Build prompt
            prompt = build_draft_prompt(
                recipient=recipient,
                subject=subject,
                body=body,
                priority=priority,
            )

            # Generate email
            response = await self.llm.generate(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=prompt,
            )

            generated_subject = subject
            generated_body = response

            # Extract subject if model returned one
            if "Subject:" in response:

                lines = response.splitlines()

                for index, line in enumerate(lines):

                    if line.lower().startswith("subject:"):
                        generated_subject = (
                            line.replace("Subject:", "")
                            .strip()
                        )

                        remaining = lines[index + 1 :]

                        generated_body = "\n".join(remaining).strip()

                        if generated_body.startswith("Body:"):
                            generated_body = generated_body.replace(
                                "Body:",
                                "",
                                1,
                            ).strip()

                        break

            return ToolResult(
                success=True,
                message=f'📧 Email drafted for {recipient}',
                data={
                    "email_id": f"EMAIL-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "to": recipient,
                    "subject": generated_subject,
                    "body": generated_body,
                    "cc": cc,
                    "priority": priority,
                    "status": "draft",
                },
                status=ToolStatus.SUCCESS,
                display_type="card",
            )

        except Exception as e:

            return ToolResult(
                success=False,
                message="Failed to draft email.",
                data={
                    "error": str(e)
                },
                status=ToolStatus.ERROR,
            )