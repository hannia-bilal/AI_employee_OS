from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List
import uuid


@dataclass
class Lead:
    id: str
    name: str
    email: str
    company: str = ""
    phone: str = ""
    source: str = "other"
    pipeline_stage: str = "new"
    notes: List[str] = field(default_factory=list)


class LeadManager:
    def __init__(self) -> None:
        self._leads: Dict[str, Lead] = {}

    def create_lead(self, data: Dict[str, str]) -> Lead:
        lead = Lead(
            id=str(data.get("id") or f"LEAD-{uuid.uuid4().hex[:8].upper()}"),
            name=str(data.get("name", "")).strip() or "Unknown Lead",
            email=str(data.get("email", "")).strip(),
            company=str(data.get("company", "")).strip(),
            phone=str(data.get("phone", "")).strip(),
            source=str(data.get("source", "other")).strip().lower() or "other",
            pipeline_stage="new",
        )
        self._leads[lead.id] = lead
        return lead

    def get_lead(self, lead_id: str) -> Lead | None:
        return self._leads.get(lead_id)

    def list_leads(self) -> List[Lead]:
        return list(self._leads.values())

    def update_lead(self, lead_id: str, data: Dict[str, str]) -> Lead | None:
        lead = self._leads.get(lead_id)
        if not lead:
            return None

        if "name" in data:
            lead.name = str(data["name"]).strip() or lead.name
        if "email" in data:
            lead.email = str(data["email"]).strip()
        if "company" in data:
            lead.company = str(data["company"]).strip()
        if "phone" in data:
            lead.phone = str(data["phone"]).strip()
        if "source" in data:
            lead.source = str(data["source"]).strip().lower() or lead.source
        if "pipeline_stage" in data:
            lead.pipeline_stage = str(data["pipeline_stage"]).strip().lower() or lead.pipeline_stage
        if "notes" in data:
            lead.notes.append(str(data["notes"]).strip())
        return lead
