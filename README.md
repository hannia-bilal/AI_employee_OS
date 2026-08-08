# AI Employee OS

AI Employee OS is an AI-powered business operating system designed to replace repetitive office work with intelligent AI agents. It serves as an **AI workforce** for companies, where specialized AI employees handle daily operations.

## Main Features

- **AI Executive Assistant**: Natural language understanding, multi-step reasoning.
- **AI Email Assistant**: Draft, reply, and summarize emails.
- **AI WhatsApp Assistant**: Send customer support messages and order confirmations.
- **AI CRM**: Manage leads, customers, and sales pipelines.
- **AI Quotation & Invoice Generator**: Create professional PDFs and payment links.
- **AI Meeting Assistant**: Audio transcription and summary extraction.
- **AI Document Intelligence**: OCR capabilities and company knowledge Q&A.
- **AI Task Manager**: Assign tasks, set deadlines, and track progress.
- **AI Reporting**: Generate sales and expense analytics.

## Technology Stack

- **Frontend**: Next.js, React, TypeScript, Tailwind CSS
- **Backend**: Python, FastAPI, SQLAlchemy
- **Database**: SQLite (Development) -> PostgreSQL (Production ready)
- **AI Engine**: LangChain, Groq API (Llama3)

## Running the Application

### 1. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## API Key Configuration (Activating Real Integrations)

The system is built to be **fully functional out of the box** using a mock database execution layer. However, to connect the AI Employees to the real world, you must configure third-party APIs. 

1. Copy `backend/.env.example` to `backend/.env`.
2. Fill in the empty API keys.
3. The system will automatically detect the keys and switch from "Mock Mode" to "Live Mode" for those specific tools.

### Required APIs:
- **Groq API**: Core LLM engine (Required).
- **OpenAI API**: For Whisper (Audio Transcription) and OCR (Document Intelligence).
- **WhatsApp Cloud API**: For the WhatsApp Assistant to send real messages.
- **Stripe API**: For the Invoice Generator to create real payment links.
- **SendGrid API**: For the Email Assistant to send real emails.
- **AWS S3**: For storing generated PDFs (Quotations/Invoices).

## Roles & Specializations

You can interact with different AI Employees by navigating to the **AI Employees** tab and selecting a persona:
- **AI CEO Assistant**: Full system access, focus on strategy and reporting.
- **AI Sales Manager**: Access to CRM and Quotations.
- **AI HR Assistant**: Access to Tasks and Meetings.
- **AI Customer Support Agent**: Access to WhatsApp and Email modules.
- **AI Finance Assistant**: Access to Invoices and Reporting.
