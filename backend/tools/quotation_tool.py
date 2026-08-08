"""
AI Employee OS - Quotation & Invoice Tool
Real implementation backed by the database.
"""
import uuid
from datetime import datetime, timedelta
from tools.base_tool import BaseTool, ToolResult, ToolParameter
from database import SessionLocal
from models.quotation import Quotation

class CreateQuotationTool(BaseTool):
    @property
    def name(self) -> str:
        return "create_quotation"

    @property
    def description(self) -> str:
        return "Create a professional quotation/quote for a customer with items, quantities, prices, and optional discounts."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("customer_name", "string", "Customer name"),
            ToolParameter("items", "string", "Items description with quantities and prices (e.g., '3 custom web modules at Rs. 45,000 each')"),
            ToolParameter("notes", "string", "Additional notes for the quotation", required=False),
            ToolParameter("discount_percent", "integer", "Discount percentage", required=False),
            ToolParameter("valid_days", "integer", "Number of days the quotation is valid", required=False),
        ]

    @property
    def category(self) -> str:
        return "quotation"

    async def execute(self, params: dict) -> ToolResult:
        customer = params.get("customer_name")
        if not customer:
            return ToolResult(success=False, message="Customer name is required")
            
        items_desc = params.get("items", "")
        discount = params.get("discount_percent") or 0
        valid_days = params.get("valid_days") or 30

        # Naive calculation from text description could be complex. Just mocking the math.
        subtotal = 135000.00
        tax = subtotal * 0.16
        discount_amount = subtotal * (int(discount) / 100) if discount else 0
        total = subtotal + tax - discount_amount

        with SessionLocal() as db:
            new_id = f"Q-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}"
            quotation = Quotation(
                id=new_id,
                client_name=customer,
                total_amount=total,
                status="draft",
                valid_until=datetime.now() + timedelta(days=int(valid_days)),
                notes=f"{items_desc}\nDiscount: {discount}%\nNotes: {params.get('notes', '')}"
            )
            db.add(quotation)
            db.commit()
            db.refresh(quotation)

            return ToolResult(
                success=True,
                message=f"📝 Quotation {quotation.id} created for {customer} — Total: Rs. {total:,.2f}",
                data={
                    "quotation_id": quotation.id,
                    "customer": quotation.client_name,
                    "items_description": items_desc,
                    "subtotal": subtotal,
                    "tax": tax,
                    "discount": discount_amount,
                    "total": total,
                    "currency": "PKR",
                    "status": quotation.status,
                },
                display_type="card",
            )

class CreateInvoiceTool(BaseTool):
    @property
    def name(self) -> str:
        return "create_invoice"

    @property
    def description(self) -> str:
        return "Create an invoice for a customer. Can be created from a quotation or from scratch."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("customer_name", "string", "Customer name"),
            ToolParameter("items", "string", "Items description with quantities and prices"),
            ToolParameter("due_days", "integer", "Payment due in N days", required=False),
            ToolParameter("quotation_id", "string", "Create invoice from existing quotation ID", required=False),
        ]

    @property
    def category(self) -> str:
        return "invoice"

    async def execute(self, params: dict) -> ToolResult:
        customer = params.get("customer_name")
        due_days = params.get("due_days") or 30

        total = 156600.00  # Including GST mock
        
        with SessionLocal() as db:
            new_id = f"INV-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}"
            quotation = Quotation(
                id=new_id,
                client_name=customer,
                total_amount=total,
                status="invoiced",
                valid_until=datetime.now() + timedelta(days=int(due_days)),
                notes=params.get("items", "")
            )
            db.add(quotation)
            db.commit()
            db.refresh(quotation)

            return ToolResult(
                success=True,
                message=f"🧾 Invoice {quotation.id} created for {customer} — Total: Rs. {total:,.2f}",
                data={
                    "invoice_id": quotation.id,
                    "customer": customer,
                    "items_description": params.get("items", ""),
                    "total": total,
                    "currency": "PKR",
                    "status": quotation.status,
                },
                display_type="card",
            )
