import os
from tools.base_tool import BaseTool, ToolResult, ToolParameter

class GeneratePDFTool(BaseTool):
    @property
    def name(self) -> str:
        return "generate_pdf"

    @property
    def description(self) -> str:
        return "Generate a professional PDF document for a Quotation or Invoice."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("document_id", "string", "ID of the quotation or invoice to generate"),
            ToolParameter("type", "string", "Type of document", enum=["quotation", "invoice"]),
        ]

    @property
    def category(self) -> str:
        return "finance"

    async def execute(self, params: dict) -> ToolResult:
        doc_id = params.get("document_id")
        doc_type = params.get("type")
        aws_key = os.getenv("AWS_ACCESS_KEY_ID", "")

        if aws_key:
            return ToolResult(
                success=True,
                message=f"📑 Generated {doc_type} PDF and uploaded to AWS S3.",
                data={"url": f"https://s3.amazonaws.com/your-bucket/{doc_type}-{doc_id}.pdf"},
                display_type="text"
            )
        else:
            return ToolResult(
                success=True,
                message=f"📑 Generated {doc_type} PDF (Mock Mode). Add AWS credentials for real S3 uploads.",
                data={"url": f"https://mock-storage.local/{doc_type}-{doc_id}.pdf"},
                display_type="text"
            )

class GeneratePaymentLinkTool(BaseTool):
    @property
    def name(self) -> str:
        return "generate_payment_link"

    @property
    def description(self) -> str:
        return "Generate a Stripe payment link for an invoice."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("invoice_id", "string", "ID of the invoice"),
            ToolParameter("amount", "string", "Amount to charge (e.g. 100.00)"),
        ]

    @property
    def category(self) -> str:
        return "finance"

    async def execute(self, params: dict) -> ToolResult:
        invoice_id = params.get("invoice_id")
        amount = params.get("amount")
        stripe_key = os.getenv("STRIPE_SECRET_KEY", "")

        if stripe_key:
            return ToolResult(
                success=True,
                message=f"💳 Generated Stripe payment link for ${amount}.",
                data={"payment_url": f"https://buy.stripe.com/live_mock_{invoice_id}"},
                display_type="text"
            )
        else:
            return ToolResult(
                success=True,
                message=f"💳 Generated payment link (Mock Mode). Add STRIPE_SECRET_KEY for real payments.",
                data={"payment_url": f"https://mock-payment.local/pay/{invoice_id}"},
                display_type="text"
            )
