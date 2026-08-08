"""
AI Employee OS - Quotation Models
Database models for Hassan's Quotations module.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON
from datetime import datetime, timezone
from database import Base

class Quotation(Base):
    __tablename__ = "quotations"

    id = Column(String(50), primary_key=True, index=True)
    client_name = Column(String(100), nullable=False)
    client_email = Column(String(100), nullable=True)
    total_amount = Column(Float, default=0.0)
    status = Column(String(50), default="draft")  # draft, sent, accepted, rejected
    valid_until = Column(DateTime, nullable=True)
    line_items = Column(JSON, default=list)  # list of dicts with description, quantity, price
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
