from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.document import Document
from schemas.modules import DocumentCreate, DocumentResponse
from elasticsearch_client import es_client

router = APIRouter(prefix="/api/documents", tags=["Documents"])

@router.get("/", response_model=List[DocumentResponse])
def get_documents(db: Session = Depends(get_db)):
    return db.query(Document).order_by(Document.created_at.desc()).all()

@router.post("/", response_model=DocumentResponse)
def create_document(document: DocumentCreate, db: Session = Depends(get_db)):
    db_document = Document(**document.model_dump())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    # Index in Elasticsearch
    es_client.index_document("documents", str(db_document.id), {
        "title": db_document.title,
        "content": db_document.content,
        "author": db_document.author,
        "document_type": db_document.document_type
    })
    
    return db_document

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document
