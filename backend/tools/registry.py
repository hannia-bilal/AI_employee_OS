"""
AI Employee OS - Tool Registry
Discovers, registers, and manages all available tools.
The AI agent uses this registry to find and call the right tool.
"""
from typing import Optional
from tools.base_tool import BaseTool, ToolResult


class ToolRegistry:
    """
    Central registry for all tools.
    
    Usage:
        registry = ToolRegistry()
        registry.register(SendEmailTool())
        registry.register(CreateQuotationTool())
        
        # AI agent uses this to find tools
        tool = registry.get_tool("send_email")
        result = await tool.execute({"to": "client@stellaris.io", ...})
    """

    def __init__(self):
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """Register a tool instance"""
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered")
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name"""
        return self._tools.get(name)

    def list_tools(self) -> list[BaseTool]:
        """List all registered tools"""
        return list(self._tools.values())

    def list_tool_names(self) -> list[str]:
        """List all registered tool names"""
        return list(self._tools.keys())

    def get_tools_by_category(self, category: str) -> list[BaseTool]:
        """Get all tools in a specific category"""
        return [t for t in self._tools.values() if t.category == category]

    def get_all_schemas(self) -> list[dict]:
        """Get JSON schemas for all tools — used for AI function calling"""
        return [tool.get_schema() for tool in self._tools.values()]

    def get_tool_descriptions(self) -> str:
        """Get formatted descriptions of all tools — used in AI system prompt"""
        lines = []
        for tool in self._tools.values():
            params = ", ".join(
                f"{p.name}: {p.type}" + (" (optional)" if not p.required else "")
                for p in tool.parameters
            )
            lines.append(f"- **{tool.name}**: {tool.description}")
            if params:
                lines.append(f"  Parameters: {params}")
        return "\n".join(lines)


# Global registry instance
tool_registry = ToolRegistry()
