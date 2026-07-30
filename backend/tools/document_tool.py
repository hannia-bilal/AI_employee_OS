"""
AI Employee OS - Document Intelligence Tool (Stub)
Module Owner: Absar Akbar
Status: STUB — Replace with real implementation

HOW TO REPLACE:
  1. Keep the same file name: document_tool.py
  2. Keep the same class names: SearchDocumentTool, AnswerFromDocsTool
  3. Keep the same .name property values: "search_documents", "answer_from_docs"
  4. Implement real logic in execute() — just return a ToolResult
  5. Remove is_mock from the data dict
  6. Drop this file into tools/ and restart the server
"""
from tools.base_tool import BaseTool, ToolResult, ToolParameter


class SearchDocumentTool(BaseTool):
    @property
    def name(self) -> str:
        return "search_documents"

    @property
    def description(self) -> str:
        return "Search company documents, files, and knowledge base for relevant information."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("query", "string", "Search query or question about company documents"),
        ]

    @property
    def category(self) -> str:
        return "document"

    async def execute(self, params: dict) -> ToolResult:
        query = params.get("query", "")
        return ToolResult(
            success=True,
            message=f'📄 Found 3 documents matching "{query}"',
            data={
                "is_mock": True,
                "results": [
                    {"title": "Company Policy Manual 2026", "type": "pdf", "relevance": 0.95, "snippet": "Section 4.2 covers the requested topic..."},
                    {"title": "Q2 Sales Report", "type": "xlsx", "relevance": 0.82, "snippet": "Revenue growth of 23% compared to Q1..."},
                    {"title": "Employee Handbook", "type": "pdf", "relevance": 0.71, "snippet": "Remote work policy updated in March 2026..."},
                ],
                "total_results": 3,
            },
            display_type="table",
        )


class AnswerFromDocsTool(BaseTool):
    @property
    def name(self) -> str:
        return "answer_from_docs"

    @property
    def description(self) -> str:
        return "Answer a question using the company knowledge base and document intelligence."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("question", "string", "Question to answer from company documents"),
        ]

    @property
    def category(self) -> str:
        return "document"

    async def execute(self, params: dict) -> ToolResult:
        question = params.get("question", "")
        return ToolResult(
            success=True,
            message="📚 Answer found from company knowledge base",
            data={
                "is_mock": True,
                "answer": "Based on the Company Policy Manual (Section 4.2), employees are entitled to 20 days of annual leave. Remote work is permitted 3 days per week with manager approval.",
                "sources": ["Company Policy Manual 2026 - Section 4.2", "Employee Handbook - Chapter 3"],
                "confidence": 0.92,
            },
            display_type="card",
        )
