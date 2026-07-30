"""
AI Employee OS - Base Tool Interface
==============================================
This is the STANDARD INTERFACE that all teammate modules must implement.
Share this file with your team so they build compatible tools.

Every tool must:
1. Inherit from BaseTool
2. Define name, description, and parameters
3. Implement the execute() method
4. Return a ToolResult
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional
from enum import Enum


class ToolStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    PENDING = "pending"
    REQUIRES_CONFIRMATION = "requires_confirmation"


@dataclass
class ToolResult:
    """Standard result returned by every tool execution"""
    success: bool
    message: str  # Human-readable result message
    data: dict = field(default_factory=dict)  # Structured data (optional)
    status: ToolStatus = ToolStatus.SUCCESS
    display_type: str = "text"  # How the frontend should render: "text", "card", "table", "pdf"

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "status": self.status.value,
            "display_type": self.display_type,
        }


@dataclass
class ToolParameter:
    """Describes a single parameter for a tool"""
    name: str
    type: str  # "string", "integer", "float", "boolean", "array", "object"
    description: str
    required: bool = True
    default: Any = None
    enum: Optional[list] = None  # Allowed values


class BaseTool(ABC):
    """
    Abstract base class for all AI Employee OS tools.
    
    Every teammate must implement this interface for their module.
    
    Example:
        class SendEmailTool(BaseTool):
            name = "send_email"
            description = "Send an email to a recipient"
            parameters = [
                ToolParameter("to", "string", "Recipient email address"),
                ToolParameter("subject", "string", "Email subject"),
                ToolParameter("body", "string", "Email body content"),
            ]
            
            async def execute(self, params: dict) -> ToolResult:
                # Your email sending logic here
                return ToolResult(success=True, message="Email sent to client@stellaris.io")
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique tool identifier, e.g., 'send_email', 'create_quotation'"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """What this tool does — used by the AI to decide when to call it"""
        pass

    @property
    @abstractmethod
    def parameters(self) -> list[ToolParameter]:
        """List of parameters this tool accepts"""
        pass

    @property
    def category(self) -> str:
        """Tool category for grouping in UI: 'email', 'crm', 'quotation', 'invoice', 'task', 'document', 'general'"""
        return "general"

    @abstractmethod
    async def execute(self, params: dict) -> ToolResult:
        """
        Execute the tool with the given parameters.
        
        Args:
            params: Dictionary of parameter values matching the parameters schema
            
        Returns:
            ToolResult with success status, message, and optional data
        """
        pass

    def get_schema(self) -> dict:
        """Generate JSON schema for AI function calling"""
        properties = {}
        required = []
        for param in self.parameters:
            prop = {
                "type": param.type,
                "description": param.description,
            }
            if param.enum:
                prop["enum"] = param.enum
            if param.default is not None:
                prop["default"] = param.default
            properties[param.name] = prop
            if param.required:
                required.append(param.name)

        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
            },
        }

    def validate_params(self, params: dict) -> tuple[bool, str]:
        """Validate parameters before execution"""
        for param in self.parameters:
            if param.required and param.name not in params:
                return False, f"Missing required parameter: {param.name}"
        return True, "Valid"
