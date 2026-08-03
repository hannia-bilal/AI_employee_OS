from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.base_tool import BaseTool, ToolParameter, ToolResult
from CRM.src.modules.activity_timeline.timeline_manager import TimelineManager
from CRM.src.modules.customer_summaries.summary_manager import CustomerSummaryManager
from CRM.src.modules.lead_management.lead_manager import LeadManager
from CRM.src.modules.sales_pipeline.pipeline_manager import SalesPipelineManager


lead_manager = LeadManager()
pipeline_manager = SalesPipelineManager()
timeline_manager = TimelineManager()
summary_manager = CustomerSummaryManager()


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
        query = str(params.get("query", "")).strip().lower()
        matches = []

        for lead in lead_manager.list_leads():
            searchable = " ".join(
                [lead.name, lead.email, lead.company, lead.phone]
            ).lower()
            if query in searchable:
                matches.append(lead)

        if not matches:
            return ToolResult(
                success=False,
                message=f'No customer found for "{query or "your search"}".',
                data={"query": query},
                display_type="text",
            )

        lead = matches[0]
        recent_activities = timeline_manager.list_activities_for_lead(lead.id)
        summary = summary_manager.generate_summary(lead.id, recent_activities)

        return ToolResult(
            success=True,
            message=f'👤 Found customer {lead.name}',
            data={
                "customer_id": lead.id,
                "name": lead.name,
                "email": lead.email,
                "company": lead.company,
                "phone": lead.phone,
                "source": lead.source,
                "pipeline_stage": lead.pipeline_stage,
                "notes": lead.notes,
                "summary": summary,
                "last_updated": datetime.now().isoformat(),
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
        lead = lead_manager.create_lead(
            {
                "name": params.get("name", "Unknown"),
                "email": params.get("email", ""),
                "company": params.get("company", ""),
                "phone": params.get("phone", ""),
                "source": params.get("source", "other"),
            }
        )
        pipeline_manager.add_deal(lead.id, lead.name, 0, lead.pipeline_stage)
        timeline_manager.add_activity(
            {
                "lead_id": lead.id,
                "title": "Lead created",
                "description": f"Created lead for {lead.name} from {lead.source}.",
                "activity_type": "note",
            }
        )

        return ToolResult(
            success=True,
            message=f"✅ New lead created: {lead.name}",
            data={
                "customer_id": lead.id,
                "name": lead.name,
                "email": lead.email,
                "company": lead.company,
                "phone": lead.phone,
                "source": lead.source,
                "pipeline_stage": lead.pipeline_stage,
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
        customer_id = str(params.get("customer_id", "")).strip()
        field = str(params.get("field", "notes")).strip()
        value = str(params.get("value", "")).strip()

        lead = lead_manager.get_lead(customer_id)
        if not lead:
            matches = [candidate for candidate in lead_manager.list_leads() if customer_id.lower() in candidate.name.lower()]
            lead = matches[0] if matches else None

        if not lead:
            return ToolResult(
                success=False,
                message=f"No customer found for '{customer_id}'.",
                data={"customer_id": customer_id},
                display_type="text",
            )

        if field == "pipeline_stage":
            lead_manager.update_lead(lead.id, {"pipeline_stage": value})
            pipeline_manager.update_stage(lead.id, value)
        elif field == "notes":
            lead_manager.update_lead(lead.id, {"notes": value})
        elif field == "email":
            lead_manager.update_lead(lead.id, {"email": value})
        elif field == "phone":
            lead_manager.update_lead(lead.id, {"phone": value})
        elif field == "company":
            lead_manager.update_lead(lead.id, {"company": value})
        elif field == "status":
            lead_manager.update_lead(lead.id, {"notes": f"Status updated to {value}"})

        timeline_manager.add_activity(
            {
                "lead_id": lead.id,
                "title": f"Updated {field}",
                "description": f"Changed {field} to {value}.",
                "activity_type": "note",
            }
        )

        return ToolResult(
            success=True,
            message=f'✅ CRM updated: {field} → "{value}" for {lead.name}',
            data={
                "customer_id": lead.id,
                "updated_field": field,
                "new_value": value,
                "updated_at": datetime.now().isoformat(),
            },
            display_type="text",
        )
