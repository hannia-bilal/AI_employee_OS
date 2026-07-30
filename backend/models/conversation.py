"""
AI Employee OS - Conversation & Message Models
Stores chat history between users and AI agents
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), default="New Conversation")
    ai_employee_id = Column(Integer, ForeignKey("ai_employees.id"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)

    # Relationships
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    ai_employee = relationship("AIEmployee", back_populates="conversations")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String(20), nullable=False)  # "user", "assistant", "system"
    content = Column(Text, nullable=False)
    metadata_ = Column("metadata", JSON, nullable=True)  # Extra data (tool results, intents, etc.)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
