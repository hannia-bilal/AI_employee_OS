"""
AI Employee OS - Main Application Entry Point
=============================================
FastAPI application that serves as the backend for AI Employee OS.

Run with: uvicorn main:app --reload --port 8000
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import init_db

# Import models so Base.metadata.create_all() can discover them
import models  # noqa: F401

# Import routers
from routers.assistant import router as assistant_router
from routers.dashboard import router as dashboard_router
from routers.crm import router as crm_router
from routers.email import router as email_router
from routers.quotation import router as quotation_router
from routers.document import router as document_router
from routers.task import router as task_router

# Import and register tools
from tools.registry import tool_registry
from tools.email_tool import DraftEmailTool, SendEmailTool, SummarizeEmailTool
from tools.crm_tool import FindCustomerTool, CreateLeadTool, UpdateCRMTool
from tools.quotation_tool import CreateQuotationTool, CreateInvoiceTool
from tools.document_tool import SearchDocumentTool, AnswerFromDocsTool
from tools.task_tool import CreateTaskTool, ScheduleMeetingTool, SetReminderTool
from tools.whatsapp_tool import SendWhatsAppTool, SummarizeWhatsAppTool
from tools.report_tool import GenerateReportTool
from tools.audio_ocr_tool import TranscribeAudioTool, ExtractTextFromImageTool
from tools.finance_tool import GeneratePDFTool, GeneratePaymentLinkTool

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def register_tools():
    """
    Register all available tools with the tool registry.
    
    ╔═══════════════════════════════════════════════════════════════════╗
    ║  TEAMMATE MODULE INTEGRATION GUIDE                              ║
    ╠═══════════════════════════════════════════════════════════════════╣
    ║  To replace a mock tool with a real implementation:             ║
    ║                                                                 ║
    ║  1. Ask your teammate for their tool file (e.g., email_tool.py) ║
    ║  2. Drop it into the tools/ directory, replacing the stub       ║
    ║  3. The tool class names and .name property must stay the same  ║
    ║  4. Restart the server — that's it!                             ║
    ║                                                                 ║
    ║  The import lines below do NOT need to change as long as the    ║
    ║  teammate keeps the same class names and file names.            ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """
    tools = [
        # ──────────────────────────────────────────────────
        # Email tools (Module Owner: Taskeen Mustafa)
        # File: tools/email_tool.py
        # Status: STUB — replace with real implementation
        # ──────────────────────────────────────────────────
        DraftEmailTool(),
        SendEmailTool(),
        SummarizeEmailTool(),

        # ──────────────────────────────────────────────────
        # CRM tools (Module Owner: Faez Ahmad)
        # File: tools/crm_tool.py
        # Status: STUB — replace with real implementation
        # ──────────────────────────────────────────────────
        FindCustomerTool(),
        CreateLeadTool(),
        UpdateCRMTool(),

        # ──────────────────────────────────────────────────
        # Quotation & Invoice tools (Module Owner: Hassan Raza)
        # File: tools/quotation_tool.py
        # Status: STUB — replace with real implementation
        # ──────────────────────────────────────────────────
        CreateQuotationTool(),
        CreateInvoiceTool(),

        # ──────────────────────────────────────────────────
        # Document tools (Module Owner: Absar Akbar)
        # File: tools/document_tool.py
        # Status: STUB — replace with real implementation
        # ──────────────────────────────────────────────────
        SearchDocumentTool(),
        AnswerFromDocsTool(),

        # ──────────────────────────────────────────────────
        # Task tools (Module Owner: Ali Zafar)
        # File: tools/task_tool.py
        # Status: STUB — replace with real implementation
        # ──────────────────────────────────────────────────
        CreateTaskTool(),
        ScheduleMeetingTool(),
        SetReminderTool(),
        
        SendWhatsAppTool(),
        SummarizeWhatsAppTool(),
        GenerateReportTool(),
        
        # Advanced Integration Tools
        TranscribeAudioTool(),
        ExtractTextFromImageTool(),
        GeneratePDFTool(),
        GeneratePaymentLinkTool(),
    ]
    for tool in tools:
        tool_registry.register(tool)
    logger.info("✅ Registered %d tools: %s", len(tools), tool_registry.list_tool_names())


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle"""
    # --- Startup ---
    init_db()
    register_tools()
    logger.info("""
╔══════════════════════════════════════════════╗
║         🤖 AI Employee OS v%s            ║
║                                              ║
║  API:       http://localhost:8000             ║
║  Docs:      http://localhost:8000/docs        ║
║  AI Model:  %s       ║
║  Tools:     %d registered                     ║
╚══════════════════════════════════════════════╝
    """, settings.APP_VERSION,
        'Groq ✅' if settings.GROQ_API_KEY else 'Demo Mode (no API key)',
        len(tool_registry.list_tools()))
    
    yield  # Application runs here
    
    # --- Shutdown ---
    logger.info("🛑 AI Employee OS shutting down...")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="AI-powered business operating system — your digital workforce",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # CORS middleware for frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_URL, "http://localhost:3000", "http://localhost:3001"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers
    app.include_router(assistant_router)
    app.include_router(dashboard_router)
    app.include_router(crm_router)
    app.include_router(email_router)
    app.include_router(quotation_router)
    app.include_router(document_router)
    app.include_router(task_router)
    
    from routers.whatsapp import router as whatsapp_router
    from routers.report import router as report_router
    from routers.ai_employee import router as ai_employee_router
    app.include_router(whatsapp_router)
    app.include_router(report_router)
    app.include_router(ai_employee_router)

    @app.get("/")
    async def root():
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "status": "running",
            "docs": "/docs",
        }

    return app


app = create_app()
