"""
AI Employee OS - AI Employee Model
Configurable AI employee profiles with different roles, tools, and permissions
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


class AIEmployee(Base):
    __tablename__ = "ai_employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # e.g., "Sales Manager"
    role = Column(String(100), nullable=False)  # e.g., "sales_manager"
    avatar = Column(String(10), nullable=True)  # Emoji avatar, e.g., "💼"
    description = Column(Text, nullable=True)
    system_prompt = Column(Text, nullable=True)  # Custom personality/instructions
    allowed_tools = Column(JSON, default=list)  # List of tool names this agent can use
    personality_traits = Column(JSON, default=list)  # e.g., ["professional", "concise"]
    is_active = Column(Boolean, default=True)
    color = Column(String(7), default="#6366f1")  # Theme color for UI

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    conversations = relationship("Conversation", back_populates="ai_employee")
