# AI Employee OS - Models Package
# All models must be imported here so Base.metadata.create_all() can see them
from models.conversation import Conversation, Message
from models.agent_action import AgentAction
from models.ai_employee import AIEmployee
from models.crm import Customer
from models.email import EmailMessage
from models.quotation import Quotation
from models.document import Document
from models.task import TaskItem
from models.whatsapp import WhatsAppMessage
from models.report import Report

__all__ = ["Conversation", "Message", "AgentAction", "AIEmployee", "Customer", "EmailMessage", "Quotation", "Document", "TaskItem", "WhatsAppMessage", "Report"]
