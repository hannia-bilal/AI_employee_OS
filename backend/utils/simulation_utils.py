from tools.base_tool import ToolResult, ToolStatus
import uuid

def simulation_result(reason: str, recipient: str, subject: str, body: str) -> ToolResult:
    return ToolResult(
        success=True,
        message=f"[SIMULATION] Email prepared for {recipient}. {reason}",
        data={
            "mode": "simulation",
            "gmail_configured": False,
            "gmail_message_id": f"sim_{uuid.uuid4().hex[:8]}",
            "to": recipient,
            "subject": subject,
            "body": body,
            "status": "simulated",
            "reason": reason
        },
        status=ToolStatus.SUCCESS,
        display_type="card",
    )
