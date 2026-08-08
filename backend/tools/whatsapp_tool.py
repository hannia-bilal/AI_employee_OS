from tools.base_tool import BaseTool, ToolResult, ToolParameter
from database import SessionLocal
from models.whatsapp import WhatsAppMessage

class SendWhatsAppTool(BaseTool):
    @property
    def name(self) -> str:
        return "send_whatsapp"

    @property
    def description(self) -> str:
        return "Send a WhatsApp message to a customer or team member."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("phone_number", "string", "Recipient phone number"),
            ToolParameter("message", "string", "The message content to send"),
        ]

    @property
    def category(self) -> str:
        return "whatsapp"

    async def execute(self, params: dict) -> ToolResult:
        phone_number = params.get("phone_number")
        message = params.get("message")
        
        if not phone_number or not message:
            return ToolResult(success=False, message="phone_number and message are required")
            
        with SessionLocal() as db:
            msg = WhatsAppMessage(
                phone_number=phone_number,
                message=message,
                direction="outbound",
                status="sent"
            )
            db.add(msg)
            db.commit()
            db.refresh(msg)
            
            return ToolResult(
                success=True,
                message=f'💬 WhatsApp sent to {phone_number}',
                data={
                    "id": msg.id,
                    "phone_number": msg.phone_number,
                    "message": msg.message,
                    "status": msg.status
                },
                display_type="card"
            )

class SummarizeWhatsAppTool(BaseTool):
    @property
    def name(self) -> str:
        return "summarize_whatsapp"

    @property
    def description(self) -> str:
        return "Summarize a WhatsApp conversation history with a specific phone number."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("phone_number", "string", "The phone number of the conversation to summarize"),
        ]

    @property
    def category(self) -> str:
        return "whatsapp"

    async def execute(self, params: dict) -> ToolResult:
        phone_number = params.get("phone_number")
        
        with SessionLocal() as db:
            messages = db.query(WhatsAppMessage).filter(WhatsAppMessage.phone_number == phone_number).all()
            if not messages:
                return ToolResult(success=False, message=f"No WhatsApp history found for {phone_number}")
                
            return ToolResult(
                success=True,
                message=f"📊 Summarized {len(messages)} WhatsApp messages for {phone_number}",
                data={
                    "phone_number": phone_number,
                    "message_count": len(messages),
                    "summary": f"User has had {len(messages)} interactions."
                },
                display_type="card"
            )
