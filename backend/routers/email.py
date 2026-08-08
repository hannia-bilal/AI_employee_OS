from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.email import EmailMessage
from schemas.modules import EmailCreate, EmailResponse

router = APIRouter(prefix="/api/emails", tags=["Emails"])

@router.get("/", response_model=List[EmailResponse])
def get_emails(db: Session = Depends(get_db)):
    return db.query(EmailMessage).order_by(EmailMessage.date.desc()).all()

@router.post("/", response_model=EmailResponse)
def create_email(email: EmailCreate, db: Session = Depends(get_db)):
    db_email = EmailMessage(**email.model_dump())
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email

@router.get("/{email_id}", response_model=EmailResponse)
def get_email(email_id: int, db: Session = Depends(get_db)):
    email = db.query(EmailMessage).filter(EmailMessage.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    return email
