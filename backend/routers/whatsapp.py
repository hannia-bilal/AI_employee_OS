from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.whatsapp import WhatsAppMessage
from schemas.modules import WhatsAppCreate, WhatsAppResponse

router = APIRouter(prefix="/api/whatsapp", tags=["whatsapp"])

@router.get("/", response_model=List[WhatsAppResponse])
def get_whatsapp_messages(db: Session = Depends(get_db)):
    return db.query(WhatsAppMessage).order_by(WhatsAppMessage.created_at.desc()).all()

@router.post("/", response_model=WhatsAppResponse)
def create_whatsapp_message(message: WhatsAppCreate, db: Session = Depends(get_db)):
    db_message = WhatsAppMessage(**message.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message
