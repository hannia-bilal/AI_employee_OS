"""
AI Employee OS - Assistant Router
Main endpoint for AI chat interactions
"""
import uuid
from fastapi import APIRouter, HTTPException
from schemas.assistant import (
    ChatMessageRequest,
    ChatMessageResponse,
    ActionResult,
    ToolListResponse,
    ToolInfo,
)
from ai.agent_engine import agent_engine
from tools.registry import tool_registry


router = APIRouter(prefix="/api/assistant", tags=["AI Assistant"])


@router.post("/chat", response_model=ChatMessageResponse)
async def chat(request: ChatMessageRequest):
    """
    Send a message to the AI Executive Assistant.
    
    The AI will:
    1. Understand your intent
    2. Plan the required actions
    3. Execute tools to complete the task
    4. Return results with a human-readable response
    """
    conversation_id = request.conversation_id or str(uuid.uuid4())

    try:
        result = await agent_engine.process_message(
            message=request.message,
            conversation_id=conversation_id,
            ai_employee_name="Executive Assistant",
        )

        actions = [
            ActionResult(
                tool_name=a.get("tool_name", "unknown"),
                status=a.get("status", "error"),
                message=a.get("message", ""),
                parameters=a.get("parameters"),
                result=a.get("result"),
                execution_time_ms=a.get("execution_time_ms"),
            )
            for a in result.get("actions", [])
        ]

        return ChatMessageResponse(
            response=result.get("response", ""),
            conversation_id=conversation_id,
            actions=actions,
            intents=result.get("intents", []),
            plan=result.get("plan", []),
            execution_time_ms=result.get("execution_time_ms", 0),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent processing error: {str(e)}")


@router.get("/tools", response_model=ToolListResponse)
async def list_tools():
    """List all available tools that the AI assistant can use"""
    tools = tool_registry.list_tools()
    return ToolListResponse(
        tools=[
            ToolInfo(
                name=t.name,
                description=t.description,
                category=t.category,
                parameters=t.get_schema()["parameters"],
            )
            for t in tools
        ],
        total=len(tools),
    )


@router.get("/health")
async def health():
    """Check AI assistant health status"""
    has_ai = agent_engine.model is not None
    return {
        "status": "healthy",
        "ai_model": "gemini" if has_ai else "rule-based (demo mode)",
        "ai_available": has_ai,
        "tools_count": len(tool_registry.list_tools()),
        "tools": tool_registry.list_tool_names(),
    }
