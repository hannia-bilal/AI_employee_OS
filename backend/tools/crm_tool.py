"""
AI Employee OS - CRM Tool
Real implementation backed by the database.
"""
import uuid
from datetime import datetime, timezone
from tools.base_tool import BaseTool, ToolResult, ToolParameter
from database import SessionLocal
from models.crm import Customer

class FindCustomerTool(BaseTool):
    @property
    def name(self) -> str:
        return "find_customer"

    @property
    def description(self) -> str:
        return "Search for a customer by name, email, or company. Returns customer details and recent activity."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("query", "string", "Customer name, email, or company to search for"),
        ]

    @property
    def category(self) -> str:
        return "crm"

    async def execute(self, params: dict) -> ToolResult:
        query = params.get("query", "").lower()
        if not query:
            return ToolResult(success=False, message="Query parameter is required")
            
        with SessionLocal() as db:
            # Search by name, email, or company
            customers = db.query(Customer).filter(
                (Customer.name.ilike(f"%{query}%")) |
                (Customer.email.ilike(f"%{query}%")) |
                (Customer.company.ilike(f"%{query}%"))
            ).all()
            
            if not customers:
                return ToolResult(
                    success=False,
                    message=f'❌ No customer found matching "{query}"'
                )
                
            # For simplicity, return the first match
            customer = customers[0]
            data = {
                "customer_id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "company": customer.company,
                "phone": customer.phone,
                "status": customer.status,
                "total_revenue": customer.total_revenue,
                "pipeline_stage": customer.pipeline_stage,
                "notes": customer.notes,
            }
            
            return ToolResult(
                success=True,
                message=f'👤 Found customer matching "{query}"',
                data=data,
                display_type="card",
            )

class CreateLeadTool(BaseTool):
    @property
    def name(self) -> str:
        return "create_lead"

    @property
    def description(self) -> str:
        return "Create a new lead/customer in the CRM system with contact information."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("name", "string", "Customer full name"),
            ToolParameter("email", "string", "Customer email address"),
            ToolParameter("company", "string", "Company name", required=False),
            ToolParameter("phone", "string", "Phone number", required=False),
            ToolParameter("source", "string", "Lead source", required=False, enum=["website", "referral", "cold_call", "social_media", "other"]),
        ]

    @property
    def category(self) -> str:
        return "crm"

    async def execute(self, params: dict) -> ToolResult:
        name = params.get("name")
        if not name:
            return ToolResult(success=False, message="Name is required to create a lead")
            
        with SessionLocal() as db:
            new_id = f"CUST-{uuid.uuid4().hex[:8].upper()}"
            customer = Customer(
                id=new_id,
                name=name,
                email=params.get("email"),
                company=params.get("company"),
                phone=params.get("phone"),
                source=params.get("source", "other"),
                pipeline_stage="new"
            )
            db.add(customer)
            db.commit()
            db.refresh(customer)
            
            data = {
                "customer_id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "company": customer.company,
                "phone": customer.phone,
                "source": customer.source,
                "pipeline_stage": customer.pipeline_stage,
            }
            
            return ToolResult(
                success=True,
                message=f"✅ New lead created: {name} (ID: {customer.id})",
                data=data,
                display_type="card",
            )

class UpdateCRMTool(BaseTool):
    @property
    def name(self) -> str:
        return "update_crm"

    @property
    def description(self) -> str:
        return "Update a customer record in the CRM. Can update pipeline stage, notes, contact info, etc."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("customer_id", "string", "Customer ID or name to update"),
            ToolParameter("field", "string", "Field to update", enum=["pipeline_stage", "notes", "email", "phone", "company", "status"]),
            ToolParameter("value", "string", "New value for the field"),
        ]

    @property
    def category(self) -> str:
        return "crm"

    async def execute(self, params: dict) -> ToolResult:
        customer_id_or_name = params.get("customer_id")
        field = params.get("field")
        value = params.get("value", "")
        
        if not customer_id_or_name or not field:
            return ToolResult(success=False, message="customer_id and field are required")
            
        with SessionLocal() as db:
            # Try to find by ID first, then by name
            customer = db.query(Customer).filter(Customer.id == customer_id_or_name).first()
            if not customer:
                customer = db.query(Customer).filter(Customer.name.ilike(f"%{customer_id_or_name}%")).first()
                
            if not customer:
                return ToolResult(success=False, message=f"❌ Customer not found: {customer_id_or_name}")
                
            # Update the field dynamically
            if hasattr(customer, field):
                setattr(customer, field, value)
                db.commit()
                db.refresh(customer)
                
                return ToolResult(
                    success=True,
                    message=f'✅ CRM updated: {field} → "{value}" for {customer.name}',
                    data={
                        "customer_id": customer.id,
                        "name": customer.name,
                        "updated_field": field,
                        "new_value": value,
                    },
                    display_type="text",
                )
            else:
                return ToolResult(success=False, message=f"❌ Invalid field: {field}")
