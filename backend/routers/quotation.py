from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.quotation import Quotation
from schemas.modules import QuotationCreate, QuotationResponse

router = APIRouter(prefix="/api/quotations", tags=["Quotations"])

@router.get("/", response_model=List[QuotationResponse])
def get_quotations(db: Session = Depends(get_db)):
    return db.query(Quotation).all()

@router.post("/", response_model=QuotationResponse)
def create_quotation(quotation: QuotationCreate, db: Session = Depends(get_db)):
    db_quotation = Quotation(**quotation.model_dump())
    db.add(db_quotation)
    db.commit()
    db.refresh(db_quotation)
    return db_quotation

@router.get("/{quotation_id}", response_model=QuotationResponse)
def get_quotation(quotation_id: str, db: Session = Depends(get_db)):
    quotation = db.query(Quotation).filter(Quotation.id == quotation_id).first()
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return quotation
