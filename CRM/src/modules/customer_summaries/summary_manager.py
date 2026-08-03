from __future__ import annotations

from typing import List

from CRM.src.modules.activity_timeline.timeline_manager import Activity


class CustomerSummaryManager:
    def generate_summary(self, lead_id: str, activities: List[Activity]) -> str:
        if not activities:
            return f"No activity recorded for lead {lead_id}."

        latest = activities[-1]
        lines = [
            f"Lead {lead_id}: {latest.title}",
            f"Summary: {latest.description}",
            f"Activity type: {latest.activity_type}",
        ]
        return "\n".join(lines)
