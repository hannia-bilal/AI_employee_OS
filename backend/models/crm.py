"""
AI Employee OS - CRM Models
Database models for Faez's CRM module.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from datetime import datetime, timezone
from database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), index=True)
    company = Column(String(100))
    phone = Column(String(20))
    status = Column(String(50), default="active")
    pipeline_stage = Column(String(50), default="new")
    total_revenue = Column(Float, default=0.0)
    source = Column(String(50), default="other")
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
