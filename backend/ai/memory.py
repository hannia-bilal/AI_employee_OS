import json
from typing import Optional
from redis_client import redis_client

class ConversationMemory:
    """
    Stores and manages conversation history for context-aware AI responses.
    
    Uses Redis as the primary data store (with fallback to memory dict via redis_client).
    Keeps a sliding window of messages and provides formatted context
    for the AI model.
    """

    def __init__(self, max_messages: int = 50):
        self.max_messages = max_messages
        self.prefix = "conv:"

    def _get_key(self, conversation_id: str) -> str:
        return f"{self.prefix}{conversation_id}"

    def add_message(self, conversation_id: str, role: str, content: str, metadata: Optional[dict] = None):
        """Add a message to conversation history in Redis"""
        key = self._get_key(conversation_id)
        
        # Get existing conversation
        data = redis_client.get(key)
        messages = json.loads(data) if data else []
        
        messages.append({
            "role": role,
            "content": content,
            "metadata": metadata or {},
        })

        # Trim to max messages
        if len(messages) > self.max_messages:
            messages = messages[-self.max_messages:]
            
        # Save back to Redis (with a 24-hour expiration)
        redis_client.set(key, json.dumps(messages), ex=86400)

    def get_context(self, conversation_id: str, last_n: int = 10) -> str:
        """Get formatted conversation context for the AI prompt"""
        messages = self.get_messages(conversation_id)
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
        key = self._get_key(conversation_id)
        data = redis_client.get(key)
        return json.loads(data) if data else []

    def clear(self, conversation_id: str):
        """Clear conversation history"""
        key = self._get_key(conversation_id)
        redis_client.delete(key)

# Global memory instance
conversation_memory = ConversationMemory()
