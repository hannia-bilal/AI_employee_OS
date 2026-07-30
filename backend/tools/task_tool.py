"""
AI Employee OS - Task, Meeting & Reminder Tool (Stub)
Module Owner: Ali Zafar
Status: STUB — Replace with real implementation

HOW TO REPLACE:
  1. Keep the same file name: task_tool.py
  2. Keep the same class names: CreateTaskTool, ScheduleMeetingTool, SetReminderTool
  3. Keep the same .name property values: "create_task", "schedule_meeting", "set_reminder"
  4. Implement real logic in execute() — just return a ToolResult
  5. Remove is_mock from the data dict
  6. Drop this file into tools/ and restart the server
"""
from tools.base_tool import BaseTool, ToolResult, ToolParameter
from datetime import datetime, timedelta


class CreateTaskTool(BaseTool):
    @property
    def name(self) -> str:
        return "create_task"

    @property
    def description(self) -> str:
        return "Create a new task with title, description, priority, deadline, and optional assignee."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("title", "string", "Task title"),
            ToolParameter("description", "string", "Task description", required=False),
            ToolParameter("priority", "string", "Task priority", required=False, enum=["low", "medium", "high", "urgent"]),
            ToolParameter("deadline", "string", "Task deadline (e.g., 'Friday', '2026-08-01', 'in 3 days')", required=False),
            ToolParameter("assignee", "string", "Person to assign the task to", required=False),
        ]

    @property
    def category(self) -> str:
        return "task"

    async def execute(self, params: dict) -> ToolResult:
        title = params.get("title", "Untitled Task")
        priority = params.get("priority", "medium")
        deadline = params.get("deadline", (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"))
        assignee = params.get("assignee", "Unassigned")

        task_id = f"TASK-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        return ToolResult(
            success=True,
            message=f'✅ Task created: "{title}" [{priority}] — Due: {deadline}',
            data={
                "is_mock": True,
                "task_id": task_id,
                "title": title,
                "description": params.get("description", ""),
                "priority": priority,
                "deadline": deadline,
                "assignee": assignee,
                "status": "todo",
                "created_at": datetime.now().isoformat(),
            },
            display_type="card",
        )


class ScheduleMeetingTool(BaseTool):
    @property
    def name(self) -> str:
        return "schedule_meeting"

    @property
    def description(self) -> str:
        return "Schedule a meeting or calendar event with date, time, participants, and optional agenda."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("title", "string", "Meeting title"),
            ToolParameter("date", "string", "Meeting date (e.g., 'Friday', '2026-08-01')"),
            ToolParameter("time", "string", "Meeting time (e.g., '3 PM', '15:00')", required=False),
            ToolParameter("participants", "string", "Meeting participants (comma-separated)", required=False),
            ToolParameter("agenda", "string", "Meeting agenda", required=False),
            ToolParameter("duration_minutes", "integer", "Duration in minutes", required=False),
        ]

    @property
    def category(self) -> str:
        return "task"

    async def execute(self, params: dict) -> ToolResult:
        title = params.get("title", "Meeting")
        date = params.get("date", "")
        time_str = params.get("time", "10:00 AM")

        meeting_id = f"MTG-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        return ToolResult(
            success=True,
            message=f'📅 Meeting scheduled: "{title}" on {date} at {time_str}',
            data={
                "is_mock": True,
                "meeting_id": meeting_id,
                "title": title,
                "date": date,
                "time": time_str,
                "participants": params.get("participants", ""),
                "agenda": params.get("agenda", ""),
                "duration_minutes": params.get("duration_minutes", 60),
                "status": "scheduled",
                "created_at": datetime.now().isoformat(),
            },
            display_type="card",
        )


class SetReminderTool(BaseTool):
    @property
    def name(self) -> str:
        return "set_reminder"

    @property
    def description(self) -> str:
        return "Set a reminder to follow up on something at a specific time or after a condition."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("message", "string", "What to be reminded about"),
            ToolParameter("when", "string", "When to trigger the reminder (e.g., 'in 3 days', 'Friday at 9 AM')"),
        ]

    @property
    def category(self) -> str:
        return "task"

    async def execute(self, params: dict) -> ToolResult:
        message = params.get("message", "")
        when = params.get("when", "tomorrow")

        return ToolResult(
            success=True,
            message=f'⏰ Reminder set: "{message}" — {when}',
            data={
                "is_mock": True,
                "reminder_id": f"REM-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "message": message,
                "trigger_time": when,
                "status": "active",
                "created_at": datetime.now().isoformat(),
            },
            display_type="text",
        )
