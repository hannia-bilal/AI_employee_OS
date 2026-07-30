# 🔧 Tool Integration Guide for Teammates

## How the AI Agent Calls Your Module

The AI Employee OS uses a **tool-based architecture**. The AI brain (`ai/agent_engine.py`) detects what the user wants, then calls the appropriate tool. Your job is to build the tool that does the actual work.

```
User → "Send a quotation to John for 25 laptops"
                ↓
        AI Brain (intent detection)
                ↓
        Calls: create_quotation(customer_name="John", items="25 laptops", ...)
                ↓
        YOUR TOOL executes and returns a ToolResult
                ↓
        AI Brain generates response → User sees the result
```

---

## Step-by-Step: Replacing a Stub with Your Real Module

### 1. Understand the Interface

Every tool inherits from `BaseTool` and must implement:

```python
from tools.base_tool import BaseTool, ToolResult, ToolParameter

class YourTool(BaseTool):
    @property
    def name(self) -> str:
        return "your_tool_name"  # MUST match the stub's name exactly
    
    @property
    def description(self) -> str:
        return "What this tool does — the AI reads this to decide when to use it"
    
    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("param_name", "string", "What this param is for"),
            ToolParameter("optional_param", "string", "Optional thing", required=False),
        ]
    
    @property
    def category(self) -> str:
        return "your_category"  # "email", "crm", "quotation", "invoice", "task", "document"
    
    async def execute(self, params: dict) -> ToolResult:
        # YOUR REAL LOGIC HERE
        # params is a dict with the parameter values
        
        return ToolResult(
            success=True,
            message="Human-readable summary of what happened",
            data={"key": "value"},  # Structured data for the frontend
            display_type="card",    # "text", "card", "table", "pdf"
        )
```

### 2. What You MUST Keep the Same

| What | Why |
|------|-----|
| **File name** (e.g., `email_tool.py`) | `main.py` imports from this file |
| **Class names** (e.g., `SendEmailTool`) | `main.py` instantiates these classes |
| **`.name` property** (e.g., `"send_email"`) | The AI agent looks up tools by this name |

### 3. What You CAN Change

- ✅ Everything inside `execute()` — this is your implementation
- ✅ Add more parameters to `.parameters` (the AI will extract them)
- ✅ Change the `ToolResult.data` dict structure
- ✅ Add helper methods, import your own modules, use database, etc.
- ✅ Add new tool classes to your file (just register them in `main.py`)

### 4. Drop-in Replacement Steps

```bash
# 1. Copy your finished file into the tools directory
cp your_module/email_tool.py backend/tools/email_tool.py

# 2. Restart the server
uvicorn main:app --reload

# 3. That's it! Test via the Command Center
```

---

## Tool Registry

Each tool file currently has these tools:

### `email_tool.py` — Owner: Taskeen Mustafa
| Class | `.name` | Description |
|-------|---------|-------------|
| `DraftEmailTool` | `draft_email` | Draft an email |
| `SendEmailTool` | `send_email` | Send an email immediately |
| `SummarizeEmailTool` | `summarize_email` | Summarize an email thread |

### `crm_tool.py` — Owner: Faez Ahmad
| Class | `.name` | Description |
|-------|---------|-------------|
| `FindCustomerTool` | `find_customer` | Search for a customer |
| `CreateLeadTool` | `create_lead` | Create a new lead |
| `UpdateCRMTool` | `update_crm` | Update a CRM record |

### `quotation_tool.py` — Owner: Hassan Raza
| Class | `.name` | Description |
|-------|---------|-------------|
| `CreateQuotationTool` | `create_quotation` | Create a quotation |
| `CreateInvoiceTool` | `create_invoice` | Create an invoice |

### `document_tool.py` — Owner: Absar Akbar
| Class | `.name` | Description |
|-------|---------|-------------|
| `SearchDocumentTool` | `search_documents` | Search company documents |
| `AnswerFromDocsTool` | `answer_from_docs` | Answer questions from docs |

### `task_tool.py` — Owner: Ali Zafar
| Class | `.name` | Description |
|-------|---------|-------------|
| `CreateTaskTool` | `create_task` | Create a task |
| `ScheduleMeetingTool` | `schedule_meeting` | Schedule a meeting |
| `SetReminderTool` | `set_reminder` | Set a reminder |

---

## ToolResult Reference

```python
@dataclass
class ToolResult:
    success: bool           # True if the operation succeeded
    message: str            # Human-readable message (shown to user)
    data: dict = {}         # Structured data (shown in UI cards)
    status: ToolStatus = ToolStatus.SUCCESS  # success, error, pending, requires_confirmation
    display_type: str = "text"  # How frontend renders: "text", "card", "table", "pdf"
```

## ToolParameter Reference

```python
@dataclass
class ToolParameter:
    name: str               # Parameter name (used as dict key)
    type: str               # "string", "integer", "float", "boolean", "array", "object"
    description: str        # Description (AI reads this to extract values)
    required: bool = True   # Is this parameter mandatory?
    default: Any = None     # Default value if not provided
    enum: list = None       # Allowed values (e.g., ["low", "medium", "high"])
```

---

## Testing Your Tool

1. Start the backend: `uvicorn main:app --reload`
2. Open: `http://localhost:8000/docs`
3. Try the `/api/assistant/chat` endpoint
4. Or use the frontend Command Center at `http://localhost:3000/command-center`

### Direct Tool Test

```python
# In a Python script or notebook:
import asyncio
from tools.email_tool import SendEmailTool

async def test():
    tool = SendEmailTool()
    result = await tool.execute({
        "to": "test@example.com",
        "subject": "Test",
        "body": "Hello!"
    })
    print(result.success)  # True
    print(result.message)  # "✅ Email sent..."
    print(result.data)     # {...}

asyncio.run(test())
```

## Questions?
Contact Muhammad Awais (Module Integration Lead)
