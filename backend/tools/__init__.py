# AI Employee OS - Tools Package
#
# This package contains all tool implementations that the AI agent can call.
# Each file contains tools for a specific module (email, CRM, etc.).
#
# TEAMMATE INTEGRATION:
# When a teammate finishes their real module, they replace the corresponding
# file in this directory. The class names and .name property must stay the same.
# See INTEGRATION_GUIDE.md for details.

from tools.base_tool import BaseTool, ToolResult, ToolParameter, ToolStatus
from tools.registry import ToolRegistry, tool_registry

__all__ = [
    "BaseTool",
    "ToolResult",
    "ToolParameter",
    "ToolStatus",
    "ToolRegistry",
    "tool_registry",
]
