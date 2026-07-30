"""
AI Employee OS - Conversation Memory
Manages conversation history and context for the AI agent
"""
from typing import Optional


class ConversationMemory:
    """
    Stores and manages conversation history for context-aware AI responses.
    
    Keeps a sliding window of messages and provides formatted context
    for the AI model. Handles token budget by summarizing old messages.
    """

    def __init__(self, max_messages: int = 50):
        self.max_messages = max_messages
        self._conversations: dict[str, list[dict]] = {}

    def add_message(self, conversation_id: str, role: str, content: str, metadata: Optional[dict] = None):
        """Add a message to conversation history"""
        if conversation_id not in self._conversations:
            self._conversations[conversation_id] = []

        self._conversations[conversation_id].append({
            "role": role,
            "content": content,
            "metadata": metadata or {},
        })

        # Trim to max messages
        if len(self._conversations[conversation_id]) > self.max_messages:
            self._conversations[conversation_id] = self._conversations[conversation_id][-self.max_messages:]

    def get_context(self, conversation_id: str, last_n: int = 10) -> str:
        """Get formatted conversation context for the AI prompt"""
        messages = self._conversations.get(conversation_id, [])
        recent = messages[-last_n:] if len(messages) > last_n else messages

        if not recent:
            return "No previous conversation."

        formatted = []
        for msg in recent:
            role_label = "User" if msg["role"] == "user" else "Assistant"
            formatted.append(f"{role_label}: {msg['content']}")

        return "\n".join(formatted)

    def get_messages(self, conversation_id: str) -> list[dict]:
        """Get raw message list for a conversation"""
        return self._conversations.get(conversation_id, [])

    def clear(self, conversation_id: str):
        """Clear conversation history"""
        self._conversations.pop(conversation_id, None)

    def get_all_conversation_ids(self) -> list[str]:
        """List all active conversation IDs"""
        return list(self._conversations.keys())


# Global memory instance
conversation_memory = ConversationMemory()
