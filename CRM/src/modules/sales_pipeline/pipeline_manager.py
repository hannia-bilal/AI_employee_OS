from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Deal:
    lead_id: str
    customer_name: str
    amount: float
    stage: str
    notes: List[str] = field(default_factory=list)


class SalesPipelineManager:
    def __init__(self) -> None:
        self._deals: Dict[str, Deal] = {}

    def add_deal(self, lead_id: str, customer_name: str, amount: float, stage: str = "new") -> Deal:
        deal = Deal(lead_id=lead_id, customer_name=customer_name, amount=float(amount), stage=str(stage).strip().lower() or "new")
        self._deals[lead_id] = deal
        return deal

    def update_stage(self, lead_id: str, stage: str) -> Deal | None:
        deal = self._deals.get(lead_id)
        if not deal:
            return None
        deal.stage = str(stage).strip().lower() or deal.stage
        return deal

    def get_deal(self, lead_id: str) -> Deal | None:
        return self._deals.get(lead_id)

    def get_stage_summary(self) -> Dict[str, int]:
        summary: Dict[str, int] = {}
        for deal in self._deals.values():
            summary[deal.stage] = summary.get(deal.stage, 0) + 1
        return summary
