"""
AI Employee OS - Quotation & Invoice Tool (Stub)
Module Owner: Hassan Raza
Status: STUB — Replace with real implementation

HOW TO REPLACE:
  1. Keep the same file name: quotation_tool.py
  2. Keep the same class names: CreateQuotationTool, CreateInvoiceTool
  3. Keep the same .name property values: "create_quotation", "create_invoice"
  4. Implement real logic in execute() — just return a ToolResult
  5. Remove is_mock from the data dict
  6. Drop this file into tools/ and restart the server
"""
from tools.base_tool import BaseTool, ToolResult, ToolParameter
from datetime import datetime, timedelta


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
        customer = params.get("customer_name", "Customer")
        items_desc = params.get("items", "")
        discount = params.get("discount_percent") or 0
        valid_days = params.get("valid_days") or 30

        # Mock calculation
        subtotal = 135000.00
        tax = subtotal * 0.16  # 16% GST in Pakistan for IT services
        discount_amount = subtotal * (discount / 100) if discount else 0
        total = subtotal + tax - discount_amount

        quote_id = f"Q-{datetime.now().strftime('%Y%m%d')}-001"

        return ToolResult(
            success=True,
            message=f"📝 Quotation {quote_id} created for {customer} — Total: Rs. {total:,.2f}",
            data={
                "is_mock": True,
                "quotation_id": quote_id,
                "customer": customer,
                "items_description": items_desc,
                "subtotal": subtotal,
                "tax": tax,
                "discount": discount_amount,
                "total": total,
                "currency": "PKR",
                "valid_until": (datetime.now() + timedelta(days=valid_days)).strftime("%Y-%m-%d"),
                "status": "draft",
                "created_at": datetime.now().isoformat(),
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
        customer = params.get("customer_name", "Customer")
        due_days = params.get("due_days") or 30

        invoice_id = f"INV-{datetime.now().strftime('%Y%m%d')}-001"
        total = 156600.00  # Including GST

        return ToolResult(
            success=True,
            message=f"🧾 Invoice {invoice_id} created for {customer} — Total: Rs. {total:,.2f}",
            data={
                "is_mock": True,
                "invoice_id": invoice_id,
                "customer": customer,
                "items_description": params.get("items", ""),
                "total": total,
                "currency": "PKR",
                "due_date": (datetime.now() + timedelta(days=due_days)).strftime("%Y-%m-%d"),
                "status": "unpaid",
                "created_at": datetime.now().isoformat(),
            },
            display_type="card",
        )
