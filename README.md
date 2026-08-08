# AI Employee OS

AI Employee OS is a next-generation business operating system designed to automate repetitive office workflows by deploying intelligent, specialized AI agents. It serves as an **AI workforce** for companies, where specialized AI employees handle daily operations across various departments such as Sales, Customer Support, Human Resources, and Finance.

## Core Modules & Features

- **AI Executive Assistant**: The brain of the operation. Understands natural language, performs multi-step reasoning, and delegates tasks to specialized modules.
- **AI Email Assistant**: Integrates with Gmail API to draft, reply, and summarize emails.
- **AI WhatsApp Assistant**: Sends customer support messages, order confirmations, and notifications.
- **AI CRM (Customer Relationship Management)**: Manages leads, customers, and sales pipelines automatically.
- **AI Quotation & Invoice Generator**: Creates professional PDFs and payment links for finance tracking.
- **AI Meeting Assistant**: Audio transcription and summary extraction for automated meeting notes.
- **AI Document Intelligence**: Deep OCR capabilities and company knowledge Q&A powered by Elasticsearch.
- **AI Task Manager**: Assigns internal tasks, sets deadlines, and tracks progress across the team.
- **AI Reporting Engine**: Generates real-time sales and expense analytics.

## Architecture & Technology Stack

The platform is designed with a modern, scalable architecture:

- **Frontend**: Next.js, React, TypeScript, Tailwind CSS (Custom Design System)
- **Backend API**: Python, FastAPI, SQLAlchemy
- **Databases**:
  - **PostgreSQL**: Primary relational data storage for CRM, Users, Tasks, and Modules.
  - **Redis**: In-memory data structure store for caching and real-time AI conversation memory.
  - **Elasticsearch**: Vector and text search engine for Document Intelligence and fast retrieval.
- **AI Engine**: LangChain, Groq API (Llama3-70b-versatile)

## Prerequisites

Before running the application, ensure you have the following installed:
- Node.js (v18+)
- Python (3.10+)
- PostgreSQL, Redis, and Elasticsearch (running locally or via Docker)

## Installation & Setup

### 1. Backend Configuration
Navigate to the backend directory, install dependencies, and configure the environment:
```bash
cd backend
python -m venv venv
# On Windows: venv\Scripts\activate
# On Mac/Linux: source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the `backend/` directory and configure your keys:
```env
APP_NAME=AI Employee OS
DATABASE_URL=postgresql://user:password@localhost/ai_employee_db
GROQ_API_KEY=your_groq_api_key_here
REDIS_URL=redis://localhost:6379/0
ELASTICSEARCH_URL=http://localhost:9200
```

Start the backend server:
```bash
uvicorn main:app --reload
```

### 2. Frontend Configuration
Navigate to the frontend directory and install dependencies:
```bash
cd frontend
npm install
```

Start the frontend development server:
```bash
npm run dev
```

The application will now be running at `http://localhost:3000`.

## Advanced API Integrations (Optional)

The system is built to be fully functional out-of-the-box using mock integrations. However, to connect the AI Employees to the real world, you can configure third-party APIs:

- **Gmail API**: Drop your `credentials.json` into the `backend/` directory to enable real email sending.
- **OpenAI Vision/Whisper**: Add `OPENAI_API_KEY` to the `.env` file to enable live audio transcription and OCR.

## Project Contributors
- **Muhammad Awais** - AI Executive Assistant & Module Integration Lead
- **Faez Ahmed** - CRM Module
- **Taskeen Mustafa** - Email API Module Integration