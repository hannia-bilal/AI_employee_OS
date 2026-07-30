"""
AI Employee OS - API Schemas
Pydantic models for API request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# --- Assistant Schemas ---

class ChatMessageRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000, description="User message to the AI assistant")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context continuity")
    ai_employee_id: Optional[int] = Field(None, description="AI employee profile to use")


class ActionResult(BaseModel):
    tool_name: str
    status: str  # success, error
    message: str
    parameters: Optional[dict] = None
    result: Optional[dict] = None
    execution_time_ms: Optional[float] = None


class ChatMessageResponse(BaseModel):
    response: str
    conversation_id: str
    actions: list[ActionResult] = []
    intents: list[dict] = []
    plan: list[dict] = []
    execution_time_ms: float = 0


# --- Conversation Schemas ---

class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str
    message_count: int = 0
    last_message: Optional[str] = None


class ConversationListResponse(BaseModel):
    conversations: list[ConversationResponse]
    total: int


# --- AI Employee Schemas ---

class AIEmployeeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    role: str = Field(..., min_length=1, max_length=100)
    avatar: Optional[str] = "🤖"
    description: Optional[str] = None
    system_prompt: Optional[str] = None
    allowed_tools: list[str] = []
    personality_traits: list[str] = []
    color: str = "#6366f1"


class AIEmployeeResponse(BaseModel):
    id: int
    name: str
    role: str
    avatar: str
    description: Optional[str]
    allowed_tools: list[str]
    personality_traits: list[str]
    is_active: bool
    color: str
    created_at: str


class AIEmployeeListResponse(BaseModel):
    employees: list[AIEmployeeResponse]
    total: int


# --- Tool Schemas ---

class ToolInfo(BaseModel):
    name: str
    description: str
    category: str
    parameters: dict


class ToolListResponse(BaseModel):
    tools: list[ToolInfo]
    total: int


# --- Dashboard Schemas ---

class DashboardStats(BaseModel):
    actions_today: int = 0
    actions_change: str = "+0%"
    active_conversations: int = 0
    conversations_change: str = "+0"
    tasks_completed: int = 0
    tasks_change: str = "+0%"
    revenue_pipeline: str = "Rs. 0"
    revenue_change: str = "+0%"


class RecentActivity(BaseModel):
    id: str
    type: str  # "email_sent", "quotation_created", etc.
    description: str
    timestamp: str
    status: str
    icon: Optional[str] = "📝"


class AIInsight(BaseModel):
    icon: str
    text: str
    type: str


class AIEmployeeStat(BaseModel):
    name: str
    avatar: str
    status: str
    actions: int


class DashboardResponse(BaseModel):
    stats: DashboardStats
    recent_activities: list[RecentActivity] = []
    ai_insights: list[AIInsight] = []
    ai_employees: list[AIEmployeeStat] = []
