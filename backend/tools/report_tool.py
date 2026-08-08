from tools.base_tool import BaseTool, ToolResult, ToolParameter
from database import SessionLocal
from models.report import Report
import json

class GenerateReportTool(BaseTool):
    @property
    def name(self) -> str:
        return "generate_report"

    @property
    def description(self) -> str:
        return "Generate a business report (e.g. sales, revenue, expense) based on current data."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("title", "string", "Title of the report"),
            ToolParameter("report_type", "string", "Type of report", enum=["sales", "revenue", "expense", "analytics"]),
            ToolParameter("summary", "string", "A brief summary or findings of the report"),
        ]

    @property
    def category(self) -> str:
        return "reporting"

    async def execute(self, params: dict) -> ToolResult:
        title = params.get("title", "Business Report")
        report_type = params.get("report_type", "analytics")
        summary = params.get("summary", "No summary provided.")
        
        with SessionLocal() as db:
            report = Report(
                title=title,
                report_type=report_type,
                data={"summary": summary}
            )
            db.add(report)
            db.commit()
            db.refresh(report)
            
            return ToolResult(
                success=True,
                message=f'📈 Report generated: {title}',
                data={
                    "id": report.id,
                    "title": report.title,
                    "report_type": report.report_type,
                    "summary": summary
                },
                display_type="card"
            )
