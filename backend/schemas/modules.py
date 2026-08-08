from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

# CRM Schemas
class CustomerBase(BaseModel):
    name: str
    email: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[str] = "active"
    pipeline_stage: Optional[str] = "new"
    total_revenue: Optional[float] = 0.0
    source: Optional[str] = "other"
    notes: Optional[str] = None

class CustomerCreate(CustomerBase):
    id: str

class CustomerResponse(CustomerBase):
    id: str
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

# Email Schemas
class EmailBase(BaseModel):
    sender: str
    recipient: str
    subject: str
    body: str
    status: Optional[str] = "sent"
    is_read: Optional[bool] = False

class EmailCreate(EmailBase):
    pass

class EmailResponse(EmailBase):
    id: int
    date: datetime
    created_at: datetime
    class Config:
        from_attributes = True

# Quotation Schemas
class QuotationBase(BaseModel):
    client_name: str
    client_email: Optional[str] = None
    total_amount: Optional[float] = 0.0
    status: Optional[str] = "draft"
    valid_until: Optional[datetime] = None
    line_items: Optional[List[Dict[str, Any]]] = []
    notes: Optional[str] = None

class QuotationCreate(QuotationBase):
    id: str

class QuotationResponse(QuotationBase):
    id: str
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

# Document Schemas
class DocumentBase(BaseModel):
    title: str
    content: str
    author: Optional[str] = None
    document_type: Optional[str] = "note"

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

# Task Schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    assigned_to: Optional[str] = None
    status: Optional[str] = "todo"
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

# WhatsApp Schemas
class WhatsAppBase(BaseModel):
    phone_number: str
    message: str
    direction: Optional[str] = "outbound"
    status: Optional[str] = "sent"

class WhatsAppCreate(WhatsAppBase):
    pass

class WhatsAppResponse(WhatsAppBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# Report Schemas
class ReportBase(BaseModel):
    title: str
    report_type: str
    data: Optional[Any] = None

class ReportCreate(ReportBase):
    pass

class ReportResponse(ReportBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
