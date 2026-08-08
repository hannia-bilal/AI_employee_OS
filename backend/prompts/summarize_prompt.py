"""
Prompt builder for email summarization.
"""

SYSTEM_PROMPT = """
You are an executive assistant.

Summarize business emails.

Your response must contain:

Summary

Key Points

Action Items

Keep it concise and professional.
"""


def build_summary_prompt(email_content: str) -> str:

    return f"""
Summarize the following email.

Email:

{email_content}
"""