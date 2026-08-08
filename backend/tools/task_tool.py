"""
AI Employee OS - Task, Meeting & Reminder Tool
Real implementation backed by the database.
"""
from datetime import datetime, timedelta
from tools.base_tool import BaseTool, ToolResult, ToolParameter
from database import SessionLocal
from models.task import TaskItem

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
        title = params.get("title")
        if not title:
            return ToolResult(success=False, message="Title is required")
            
        description = params.get("description", "")
        priority = params.get("priority", "medium")
        deadline = params.get("deadline")
        assignee = params.get("assignee", "Unassigned")

        # Combine priority and deadline into description for now since model doesn't have them
        full_desc = f"{description}\nPriority: {priority}\nDeadline: {deadline}"

        with SessionLocal() as db:
            task = TaskItem(
                title=title,
                description=full_desc,
                assigned_to=assignee,
                status="todo"
            )
            db.add(task)
            db.commit()
            db.refresh(task)

            return ToolResult(
                success=True,
                message=f'✅ Task created: "{title}"',
                data={
                    "task_id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "assignee": task.assigned_to,
                    "status": task.status,
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
        
        desc = f"Meeting on {date} at {time_str}\nParticipants: {params.get('participants', '')}\nAgenda: {params.get('agenda', '')}"
        
        with SessionLocal() as db:
            task = TaskItem(
                title=f"Meeting: {title}",
                description=desc,
                assigned_to=params.get("participants", ""),
                status="scheduled"
            )
            db.add(task)
            db.commit()
            db.refresh(task)

            return ToolResult(
                success=True,
                message=f'📅 Meeting scheduled: "{title}" on {date} at {time_str}',
                data={
                    "meeting_id": task.id,
                    "title": task.title,
                    "date": date,
                    "time": time_str,
                    "status": task.status,
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

        with SessionLocal() as db:
            task = TaskItem(
                title=f"Reminder: {message[:20]}...",
                description=f"Remind me: {message}\nWhen: {when}",
                status="active"
            )
            db.add(task)
            db.commit()
            db.refresh(task)

            return ToolResult(
                success=True,
                message=f'⏰ Reminder set: "{message}" — {when}',
                data={
                    "reminder_id": task.id,
                    "message": message,
                    "trigger_time": when,
                    "status": task.status,
                },
                display_type="text",
            )
