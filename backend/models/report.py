from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime
from database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    report_type = Column(String(50), nullable=False) # "sales", "revenue", "expense", "analytics"
    data = Column(JSON, nullable=True) # Store analytical data as JSON for flexibility
    created_at = Column(DateTime, default=datetime.utcnow)
