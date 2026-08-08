from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.ai_employee import AIEmployee
from pydantic import BaseModel

router = APIRouter(prefix="/api/ai-employees", tags=["AI Employees"])

class AIEmployeeBase(BaseModel):
    name: str
    role: str
    avatar: Optional[str] = "🤖"
    description: Optional[str] = ""
    system_prompt: Optional[str] = ""
    allowed_tools: List[str] = []
    personality_traits: List[str] = []
    color: Optional[str] = "#6366f1"

class AIEmployeeCreate(AIEmployeeBase):
    pass

class AIEmployeeResponse(AIEmployeeBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

@router.get("", response_model=List[AIEmployeeResponse])
def get_ai_employees(db: Session = Depends(get_db)):
    employees = db.query(AIEmployee).all()
    # Add defaults if empty
    if not employees:
        default_employees = [
            AIEmployee(name="Executive Assistant", role="System Brain", avatar="🤖", description="The core AI engine.", allowed_tools=["All Tools"], color="#6366f1"),
            AIEmployee(name="Sales Manager", role="CRM & Leads", avatar="💼", description="Specializes in sales pipeline.", allowed_tools=["Find Customer", "Create Lead", "Update CRM", "Send Email"], color="#8b5cf6"),
            AIEmployee(name="Customer Support", role="Support & Docs", avatar="🎧", description="Handles incoming queries.", allowed_tools=["Search Documents", "Answer from Docs", "Send Email", "Draft Email"], color="#22c55e"),
            AIEmployee(name="Finance Assistant", role="Billing & Quotes", avatar="💰", description="Manages financial documents.", allowed_tools=["Create Quotation", "Create Invoice", "Send Email"], color="#f59e0b", is_active=False),
            AIEmployee(name="HR Assistant", role="Internal Tasks", avatar="📋", description="Manages internal tasks.", allowed_tools=["Create Task", "Schedule Meeting", "Set Reminder", "Search Documents"], color="#ef4444")
        ]
        # Quick fix to match schema
        for emp in default_employees:
            db.add(emp)
        db.commit()
        employees = db.query(AIEmployee).all()
    return employees

@router.post("", response_model=AIEmployeeResponse)
def create_ai_employee(employee: AIEmployeeCreate, db: Session = Depends(get_db)):
    db_employee = AIEmployee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee
