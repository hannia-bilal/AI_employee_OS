from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List
import uuid


@dataclass
class Activity:
    id: str
    lead_id: str
    title: str
    description: str
    activity_type: str = "note"


class TimelineManager:
    def __init__(self) -> None:
        self._activities: Dict[str, Activity] = {}

    def add_activity(self, data: Dict[str, str]) -> Activity:
        activity = Activity(
            id=str(uuid.uuid4())[:8],
            lead_id=str(data.get("lead_id", "")).strip(),
            title=str(data.get("title", "")).strip(),
            description=str(data.get("description", "")).strip(),
            activity_type=str(data.get("activity_type", "note")).strip().lower() or "note",
        )
        self._activities[activity.id] = activity
        return activity

    def list_activities_for_lead(self, lead_id: str) -> List[Activity]:
        return [activity for activity in self._activities.values() if activity.lead_id == lead_id]
