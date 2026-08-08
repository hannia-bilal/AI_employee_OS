"""
Prompt builder for email drafting.
"""


SYSTEM_PROMPT = """
You are an expert executive assistant.

Write professional business emails.

Rules:

1. Generate a concise subject.
2. Generate a professional email body.
3. Use appropriate greetings.
4. Use appropriate closing.
5. Never invent facts.
6. Keep the tone requested.
7. Return ONLY in this format:

Subject: ...

Body:
...
"""


def build_draft_prompt(
    recipient: str,
    subject: str,
    body: str,
    priority: str = "normal",
) -> str:
    return f"""
Recipient:
{recipient}

Subject:
{subject}

Body / Instructions:
{body}

Priority:
{priority}
"""