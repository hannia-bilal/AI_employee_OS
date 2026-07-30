"""
AI Employee OS - CRM Tool (Stub)
Module Owner: Faez Ahmad
Status: STUB — Replace with real implementation

HOW TO REPLACE:
  1. Keep the same file name: crm_tool.py
  2. Keep the same class names: FindCustomerTool, CreateLeadTool, UpdateCRMTool
  3. Keep the same .name property values: "find_customer", "create_lead", "update_crm"
  4. Implement real logic in execute() — just return a ToolResult
  5. Remove is_mock from the data dict
  6. Drop this file into tools/ and restart the server
"""
from tools.base_tool import BaseTool, ToolResult, ToolParameter
from datetime import datetime


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
        query = params.get("query", "")
        # STUB: Return mock customer data
        return ToolResult(
            success=True,
            message=f'👤 Found customer matching "{query}"',
            data={
                "is_mock": True,
                "customer_id": "CUST-001",
                "name": query.title() if query else "Faez Ahmad",
                "email": f"{query.lower().replace(' ', '.')}@company.com" if query else "faez.ahmad@codecelix.com",
                "company": query.title() if query else "CodeCelix",
                "phone": "+1-555-0123",
                "status": "active",
                "total_revenue": 45000,
                "last_contact": "2026-07-25",
                "pipeline_stage": "negotiation",
            },
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
        name = params.get("name", "Unknown")
        return ToolResult(
            success=True,
            message=f"✅ New lead created: {name}",
            data={
                "is_mock": True,
                "customer_id": f"CUST-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "name": name,
                "email": params.get("email", ""),
                "company": params.get("company", ""),
                "phone": params.get("phone", ""),
                "source": params.get("source", "other"),
                "pipeline_stage": "new",
                "created_at": datetime.now().isoformat(),
            },
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
        customer_id = params.get("customer_id", "CUST-001")
        field = params.get("field", "notes")
        value = params.get("value", "")
        return ToolResult(
            success=True,
            message=f'✅ CRM updated: {field} → "{value}" for {customer_id}',
            data={
                "is_mock": True,
                "customer_id": customer_id,
                "updated_field": field,
                "new_value": value,
                "updated_at": datetime.now().isoformat(),
            },
            display_type="text",
        )
