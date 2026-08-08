# Email Module Documentation

**Project:** AI Employee OS  
**Module:** Email Management  
**Owner:** Taskeen Mustafa  
**Version:** 1.0.0  
**Status:** Production Ready (Pending Gmail Credentials)

---

# Overview

The Email Module enables the AI Employee OS to perform email-related operations through a tool-based architecture.

It currently supports:

- Draft Email
- Send Email
- Summarize Email
- Gmail API Integration
- Simulation Mode (when Gmail credentials are unavailable)

The module is designed so that the AI Agent only communicates with tool classes, while all business logic resides inside service classes.

---

# Architecture

```
                User
                  │
                  ▼
          AI Executive Assistant
                  │
                  ▼
            Tool Registry
                  │
      ┌───────────┼────────────┐
      ▼           ▼            ▼
Draft Tool    Send Tool    Summary Tool
      │           │            │
      ▼           ▼            ▼
 Draft Service Send Service Summary Service
                    │
                    ▼
               Gmail Service
                    │
                    ▼
              Gmail OAuth
                    │
                    ▼
                Gmail API
```

---

# Folder Structure

```
backend/
│
├── auth/
│   ├── gmail_auth.py
│   ├── credentials.example.json
│   └── credentials.json      (Owner Only)
│
├── services/
│   ├── draft_service.py
│   ├── send_service.py
│   ├── summarize_service.py
│   └── gmail_service.py
│
├── tools/
│   ├── base_tool.py
│   └── email_tool.py
│
├── tokens/
│   ├── token.example.json
│   └── token.json            (Generated Automatically)
│
├── utils/
│   ├── gmail_utils.py
│   └── simulation_utils.py
│
├── config.py
└── requirements.txt
```

---

# Responsibilities

## email_tool.py

Contains only AI Tool definitions.

Responsibilities:

- Parameter validation
- Calling services
- Returning ToolResult

No business logic should exist here.

---

## draft_service.py

Responsible for:

- Email draft generation
- Formatting
- Returning draft metadata

Future Improvements:

- AI-generated email drafting
- Templates
- Signature support
- HTML email support

---

## send_service.py

Responsible for:

- Sending emails
- Calling GmailService
- Returning production responses
- Falling back to Simulation Mode

Current Workflow:

```
Validate Parameters
        │
        ▼
Create GmailService
        │
        ▼
Send Email
        │
        ├──── Success
        │
        └──── Failure
                 │
                 ▼
         Simulation Mode
```

---

## summarize_service.py

Responsible for:

- Email summarization
- Key points extraction
- Action item generation

Current Version:

Rule-based.

Future Version:

LLM-based summarization using Groq.

---

## gmail_service.py

Wrapper around Gmail API.

Responsibilities:

- Send Email
- Read Email
- List Emails
- Read Threads
- Delete Email

Future additions:

- Reply Email
- Forward Email
- Attachments
- Labels
- Search
- Mark Read/Unread

---

## gmail_auth.py

Handles Gmail OAuth.

Responsibilities:

- Load credentials.json
- Create token.json
- Refresh expired tokens
- Authenticate user

Only this file should manage authentication.

---

## gmail_utils.py

Utility functions.

Responsibilities:

- Parse Gmail responses
- Decode Base64 content
- Extract headers
- Convert Gmail payloads into Python dictionaries

No API calls should be placed here.

---

## simulation_utils.py

Provides a common simulation response.

Example:

```python
return simulation_result(
    reason="credentials.json not found.",
    recipient=recipient,
    subject=subject,
    body=body,
)
```

Used whenever Gmail cannot be accessed.

---

# Email Workflow

## Draft Email

```
User
 │
 ▼
AI Agent
 │
 ▼
DraftEmailTool
 │
 ▼
DraftEmailService
 │
 ▼
ToolResult
```

---

## Send Email

```
User
 │
 ▼
AI Agent
 │
 ▼
SendEmailTool
 │
 ▼
SendEmailService
 │
 ▼
GmailService
 │
 ▼
GmailAuth
 │
 ▼
Google Gmail API
```

---

## Summarize Email

```
User
 │
 ▼
AI Agent
 │
 ▼
SummarizeEmailTool
 │
 ▼
SummarizeEmailService
 │
 ▼
Summary Result
```

---

# Production vs Simulation Mode

## Production Mode

Occurs when:

- credentials.json exists
- token.json exists
- Gmail OAuth succeeds

Returns:

```
Mode: Production
Email Sent: Yes
Gmail Message ID
```

---

## Simulation Mode

Occurs when:

- credentials.json missing
- token.json missing
- OAuth failed
- Gmail unavailable

Returns:

```
Mode: Simulation

Reason:
credentials.json not found.

No email was actually sent.
```

This allows the AI Employee OS to continue functioning during development.

---

# Required Configuration

## config.py

```
GMAIL_SCOPES = (
    "https://www.googleapis.com/auth/gmail.send "
    "https://www.googleapis.com/auth/gmail.readonly"
)
```

---

# Required Files

Owner must provide:

```
backend/auth/credentials.json
```

Generated automatically:

```
backend/tokens/token.json
```

Never commit either file.

---

# Example Files

Included:

```
credentials.example.json
token.example.json
```

These contain placeholders only.

---

# Required Packages

```
google-api-python-client
google-auth
google-auth-oauthlib
google-auth-httplib2
```

---

# Error Handling

Current handling includes:

- Missing credentials.json
- Missing token.json
- Invalid token
- OAuth failure
- Gmail API errors
- Unexpected exceptions

Simulation Mode is automatically activated whenever Gmail cannot be used.

---

# Integration with AI Employee OS

The AI Engine never communicates directly with Gmail.

Flow:

```
AI Agent
      │
      ▼
Tool
      │
      ▼
Service
      │
      ▼
Gmail Service
      │
      ▼
Google API
```

This keeps business logic separated from AI logic.

---

# Future Enhancements

## Draft

- AI-generated drafts
- Templates
- HTML emails
- Attachments

---

## Send

- CC/BCC support
- Attachments
- HTML emails
- Scheduling
- Retry mechanism

---

## Summary

- Groq LLM integration
- Thread summarization
- Sentiment analysis
- Action extraction

---

## Gmail

- Reply
- Forward
- Search
- Labels
- Archive
- Star
- Read/Unread
- Trash
- Attachment download

---

# Coding Guidelines

When modifying this module:

- Do not change tool names.
- Keep BaseTool interface unchanged.
- Business logic belongs in `services/`.
- Authentication belongs only in `gmail_auth.py`.
- Gmail API calls belong only in `gmail_service.py`.
- Parsing belongs only in `gmail_utils.py`.
- Simulation responses should always use `simulation_result()`.
- Always return `ToolResult`.
- Preserve async method signatures.
- Add new functionality through services instead of expanding tool classes.

---

# Developer Notes

This module is designed to be modular, testable, and easily extendable. During development, Simulation Mode ensures the application remains fully functional even when Gmail credentials are unavailable. Once the project owner supplies valid Google OAuth credentials, the module automatically transitions to Production Mode without requiring any code changes.