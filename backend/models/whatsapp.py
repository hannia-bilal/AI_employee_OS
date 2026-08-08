from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base

class WhatsAppMessage(Base):
    __tablename__ = "whatsapp_messages"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), index=True, nullable=False)
    message = Column(Text, nullable=False)
    direction = Column(String(10), default="outbound") # "inbound" or "outbound"
    status = Column(String(20), default="sent") # "sent", "delivered", "read", "received"
    created_at = Column(DateTime, default=datetime.utcnow)
