# AI Employee OS

AI Employee OS is an AI-powered business operating system designed to replace repetitive office work with intelligent AI agents. It serves as a central platform where AI handles emails, customer communication, quotations, invoices, meeting summaries, CRM updates, task management, reporting, and workflow automation.

## Project Vision
To build the world's first AI-powered digital workforce that helps businesses automate daily operations, reduce operational costs, and improve productivity.

## 🚀 Powered by Groq API
This project leverages the lightning-fast **Groq API** (using Llama-3 models) for natural language understanding and intent routing, ensuring near-instantaneous responses and multi-step reasoning capabilities.

## Module Integration Architecture
This repository contains the core AI Executive Assistant engine. It uses a tool-based architecture where specialized AI employees can execute real business tasks.

### Features
- **AI Executive Assistant**: Understands natural language, maintains context memory, and executes multi-step workflows.
- **Dynamic Tool Registry**: Allows easy drop-in of custom modules.
- **Fallback Demo Mode**: Rule-based fallback if the API key is not configured.

## 🛠️ Setup & Run Instructions

Follow these steps to get the AI Employee OS running on your local machine.

### 1. Backend Setup (FastAPI & AI Engine)

First, install the Python dependencies listed in `requirements.txt`:

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install all required dependencies
pip install -r requirements.txt
```

#### Configure Environment
Copy `backend/.env` (if it doesn't exist, create it) and add your Groq API key:
```env
# Get a free key from https://console.groq.com
GROQ_API_KEY=your_groq_api_key_here
```

#### Run the Backend Server
```bash
uvicorn main:app --reload --port 8000
```
*API Documentation will be available at [http://localhost:8000/docs](http://localhost:8000/docs).*

### 2. Frontend Setup (Next.js Dashboard)

In a new terminal window, install the Node.js dependencies and start the UI:

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Run the development server
npm run dev
```
*The Command Center interface will be available at [http://localhost:3000](http://localhost:3000).*

## Integrating New Modules (For Teammates)
If you are developing a module (e.g., CRM, Email, Quotation), refer to the integration guide located at `backend/tools/INTEGRATION_GUIDE.md`.

Drop your implementations into the `backend/tools/` directory to have them automatically picked up by the AI Agent!

## Team
- **Muhammad Awais** - AI Executive Assistant & Module Integration Lead
- **Faez Ahmed** - Responsible for CRM Module