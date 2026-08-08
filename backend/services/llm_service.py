"""
LLM Service
-----------
Centralized wrapper for Groq API.

All AI features (draft, reply, summarize, classify, prioritize)
must use this service.
"""

from groq import Groq
from config import settings


class LLMService:
    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not configured.")

        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.AI_MODEL

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 1024,
    ) -> str:
        """
        Generic text generation.

        Returns only the generated text.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        return response.choices[0].message.content.strip()

    async def summarize(self, text: str) -> str:
        system_prompt = (
            "You are an enterprise AI assistant. "
            "Summarize emails into concise business summaries."
        )

        return await self.generate(
            system_prompt=system_prompt,
            user_prompt=text,
            temperature=0.2,
        )

    async def classify(self, text: str) -> str:
        system_prompt = """
You are an enterprise email classifier.

Choose ONLY ONE category.

Categories:
- Sales
- Support
- HR
- Finance
- Meeting
- Marketing
- Personal
- Spam
- Other

Return ONLY the category name.
"""

        return await self.generate(
            system_prompt=system_prompt,
            user_prompt=text,
            temperature=0,
            max_tokens=20,
        )

    async def prioritize(self, text: str) -> str:
        system_prompt = """
Determine the priority of the email.

Possible priorities:

Critical
High
Medium
Low

Return ONLY one word.
"""

        return await self.generate(
            system_prompt=system_prompt,
            user_prompt=text,
            temperature=0,
            max_tokens=10,
        )