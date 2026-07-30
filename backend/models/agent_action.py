"""
AI Employee OS - Agent Action Model
Logs every action the AI agent performs (tool calls, results, errors)
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


class AgentAction(Base):
    __tablename__ = "agent_actions"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=True)

    # Action details
    intent = Column(String(100), nullable=False)  # e.g., "send_email", "create_quotation"
    tool_name = Column(String(100), nullable=False)  # Which tool was called
    parameters = Column(JSON, nullable=True)  # Parameters passed to the tool
    result = Column(JSON, nullable=True)  # Tool execution result
    status = Column(String(20), default="pending")  # pending, running, success, error
    error_message = Column(Text, nullable=True)
    execution_time_ms = Column(Float, nullable=True)  # How long the tool took

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    conversation = relationship("Conversation")
