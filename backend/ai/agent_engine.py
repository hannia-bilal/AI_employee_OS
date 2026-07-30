"""
AI Employee OS - Agent Engine
============================
The CORE AI brain that powers the entire platform.

Flow:
  User Message → Intent Detection → Task Planning → Tool Execution → Response

Uses Groq API (e.g. llama3) for NLU, with graceful fallback
to rule-based intent detection when API key is not available.
"""
import json
import time
import re
import logging
from typing import Optional
from datetime import datetime, timezone

from config import settings
from ai.prompts import EXECUTIVE_ASSISTANT_SYSTEM_PROMPT, INTENT_DETECTION_PROMPT, TASK_PLANNING_PROMPT
from ai.memory import conversation_memory
from tools.registry import tool_registry
from tools.base_tool import ToolResult

logger = logging.getLogger(__name__)


class AgentEngine:
    """
    Main AI Agent Engine.
    
    Orchestrates the full flow:
    1. Receive user message
    2. Detect intent(s) using Gemini or fallback
    3. Plan multi-step tasks if needed
    4. Execute tools in order
    5. Compile and return results
    """

    def __init__(self):
        self.model = None
        self._init_ai_model()

    def _init_ai_model(self):
        """Initialize Groq AI client if API key is available"""
        if settings.GROQ_API_KEY:
            try:
                from groq import AsyncGroq
                self.model = AsyncGroq(api_key=settings.GROQ_API_KEY)
                logger.info("✅ Groq AI client initialized using model: %s", settings.AI_MODEL)
            except Exception as e:
                logger.warning("⚠️ Failed to initialize Groq: %s", e)
                self.model = None
        else:
            logger.info("ℹ️ No GROQ_API_KEY set — running in demo mode with rule-based intent detection")

    async def process_message(
        self,
        message: str,
        conversation_id: str,
        ai_employee_name: str = "Executive Assistant",
    ) -> dict:
        """
        Process a user message through the full agent pipeline.
        
        Returns:
            {
                "response": "Human-readable response text",
                "actions": [...],  # List of executed actions with results
                "intents": [...],  # Detected intents
                "plan": [...],     # Execution plan steps
            }
        """
        start_time = time.time()

        # Store user message in memory
        conversation_memory.add_message(conversation_id, "user", message)

        # Step 1: Detect intents
        intent_result = await self._detect_intents(message, conversation_id)

        # Step 2: Handle different cases
        if intent_result.get("is_general_chat"):
            response = intent_result.get("chat_response", "Hello! How can I help you today?")
            conversation_memory.add_message(conversation_id, "assistant", response)
            return {
                "response": response,
                "actions": [],
                "intents": [],
                "plan": [],
                "execution_time_ms": (time.time() - start_time) * 1000,
            }

        if intent_result.get("requires_clarification"):
            question = intent_result.get("clarification_question", "Could you please provide more details?")
            conversation_memory.add_message(conversation_id, "assistant", question)
            return {
                "response": question,
                "actions": [],
                "intents": intent_result.get("intents", []),
                "plan": [],
                "execution_time_ms": (time.time() - start_time) * 1000,
            }

        intents = intent_result.get("intents", [])
        if not intents:
            response = "I'm not sure what you'd like me to do. Could you rephrase your request? I can help with emails, quotations, invoices, tasks, meetings, and more."
            conversation_memory.add_message(conversation_id, "assistant", response)
            return {
                "response": response,
                "actions": [],
                "intents": [],
                "plan": [],
                "execution_time_ms": (time.time() - start_time) * 1000,
            }

        # Step 3: Execute tools
        actions = []
        for intent in intents:
            tool_name = intent.get("tool_name")
            params = intent.get("parameters", {})

            tool = tool_registry.get_tool(tool_name)
            if not tool:
                actions.append({
                    "tool_name": tool_name,
                    "status": "error",
                    "message": f"Tool '{tool_name}' not found in registry. Available: {tool_registry.list_tool_names()}",
                    "parameters": params,
                    "result": None,
                })
                continue

            # Validate parameters
            is_valid, validation_msg = tool.validate_params(params)
            if not is_valid:
                actions.append({
                    "tool_name": tool_name,
                    "status": "error",
                    "message": validation_msg,
                    "parameters": params,
                    "result": None,
                })
                continue

            # Execute the tool
            try:
                tool_start = time.time()
                result = await tool.execute(params)
                tool_time = (time.time() - tool_start) * 1000

                actions.append({
                    "tool_name": tool_name,
                    "status": "success" if result.success else "error",
                    "message": result.message,
                    "parameters": params,
                    "result": result.to_dict(),
                    "execution_time_ms": tool_time,
                })
            except Exception as e:
                logger.error("Tool '%s' execution failed: %s", tool_name, e, exc_info=True)
                actions.append({
                    "tool_name": tool_name,
                    "status": "error",
                    "message": f"Tool execution failed: {str(e)}",
                    "parameters": params,
                    "result": None,
                })

        # Step 4: Generate response
        response = await self._generate_response(message, actions, ai_employee_name, conversation_id)

        conversation_memory.add_message(conversation_id, "assistant", response, {"actions": actions})

        return {
            "response": response,
            "actions": actions,
            "intents": intents,
            "plan": [{"step": i + 1, "tool": a["tool_name"], "status": a["status"]} for i, a in enumerate(actions)],
            "execution_time_ms": (time.time() - start_time) * 1000,
        }

    async def _detect_intents(self, message: str, conversation_id: str) -> dict:
        """Detect user intents using Groq or fallback to rules"""
        if self.model:
            return await self._detect_intents_ai(message, conversation_id)
        else:
            return self._detect_intents_rules(message)

    async def _detect_intents_ai(self, message: str, conversation_id: str) -> dict:
        """Use Groq to detect intents — non-blocking async call"""
        try:
            context = conversation_memory.get_context(conversation_id, last_n=5)
            tool_descriptions = tool_registry.get_tool_descriptions()

            prompt = INTENT_DETECTION_PROMPT.format(
                tool_descriptions=tool_descriptions,
                user_message=message,
                context=context,
            )

            # Use async version to avoid blocking the event loop
            response = await self.model.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=settings.AI_MODEL,
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            text = response.choices[0].message.content.strip()

            # Extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', text)
            if json_match:
                parsed = json.loads(json_match.group())
                # Validate the parsed result has the expected structure
                if "intents" not in parsed and "is_general_chat" not in parsed:
                    logger.warning("Groq returned JSON without expected keys, falling back to rules")
                    return self._detect_intents_rules(message)
                return parsed
            else:
                logger.warning("Groq did not return valid JSON, falling back to rules")
                return self._detect_intents_rules(message)

        except Exception as e:
            logger.warning("⚠️ Groq intent detection failed: %s", e)
            return self._detect_intents_rules(message)

    def _detect_intents_rules(self, message: str) -> dict:
        """
        Rule-based fallback intent detection.
        Works without an AI model for demo/testing purposes.
        
        NOTE: `msg` is lowercased for keyword matching.
              `message` (original case) is used for name/parameter extraction.
        """
        msg = message.lower().strip()

        # General chat patterns
        greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "how are you", "what can you do", "help"]
        if any(msg.startswith(g) or msg == g for g in greetings):
            return {
                "is_general_chat": True,
                "chat_response": (
                    "Hello! 👋 I'm your AI Executive Assistant. I can help you with:\n\n"
                    "• 📧 **Emails** — Draft, send, or summarize emails\n"
                    "• 📝 **Quotations** — Create professional quotations\n"
                    "• 🧾 **Invoices** — Generate invoices\n"
                    "• 👤 **CRM** — Find customers, create leads\n"
                    "• ✅ **Tasks** — Create tasks and set reminders\n"
                    "• 📅 **Meetings** — Schedule meetings\n"
                    "• 📄 **Documents** — Search company knowledge base\n\n"
                    "Just tell me what you need in plain English!"
                ),
                "intents": [],
                "requires_clarification": False,
            }

        intents = []

        # Email intents
        if any(word in msg for word in ["email", "mail", "send message", "write to"]):
            if any(word in msg for word in ["summarize", "summary"]):
                intents.append({
                    "tool_name": "summarize_email",
                    "confidence": 0.8,
                    "parameters": {"email_id": "latest"},
                    "reasoning": "User wants to summarize email",
                })
            elif any(word in msg for word in ["draft"]):
                intents.append({
                    "tool_name": "draft_email",
                    "confidence": 0.85,
                    "parameters": self._extract_email_params(message),
                    "reasoning": "User wants to draft an email",
                })
            else:
                intents.append({
                    "tool_name": "send_email",
                    "confidence": 0.85,
                    "parameters": self._extract_email_params(message),
                    "reasoning": "User wants to send an email",
                })

        # Quotation intents
        if any(word in msg for word in ["quotation", "quote", "proposal", "estimate"]):
            intents.append({
                "tool_name": "create_quotation",
                "confidence": 0.9,
                "parameters": self._extract_quotation_params(message),
                "reasoning": "User wants to create a quotation",
            })

        # Invoice intents
        if any(word in msg for word in ["invoice", "bill", "billing"]):
            intents.append({
                "tool_name": "create_invoice",
                "confidence": 0.9,
                "parameters": self._extract_invoice_params(message),
                "reasoning": "User wants to create an invoice",
            })

        # CRM intents
        if any(word in msg for word in ["customer", "client", "contact", "lead"]):
            if any(word in msg for word in ["find", "search", "look up", "get", "who is"]):
                intents.append({
                    "tool_name": "find_customer",
                    "confidence": 0.85,
                    "parameters": {"query": self._extract_name(message)},
                    "reasoning": "User wants to find a customer",
                })
            elif any(word in msg for word in ["create", "add", "new", "register"]):
                intents.append({
                    "tool_name": "create_lead",
                    "confidence": 0.85,
                    "parameters": {"name": self._extract_name(message), "email": "", "company": ""},
                    "reasoning": "User wants to create a new lead",
                })
            elif any(word in msg for word in ["update", "change", "modify"]):
                intents.append({
                    "tool_name": "update_crm",
                    "confidence": 0.8,
                    "parameters": {"customer_id": self._extract_name(message), "field": "notes", "value": "Updated via AI"},
                    "reasoning": "User wants to update CRM",
                })

        # Task intents
        if any(word in msg for word in ["task", "todo", "to-do", "assign", "reminder", "remind"]):
            if any(word in msg for word in ["remind", "reminder"]):
                intents.append({
                    "tool_name": "set_reminder",
                    "confidence": 0.85,
                    "parameters": {"message": message, "when": self._extract_time(msg)},
                    "reasoning": "User wants to set a reminder",
                })
            else:
                intents.append({
                    "tool_name": "create_task",
                    "confidence": 0.85,
                    "parameters": self._extract_task_params(message),
                    "reasoning": "User wants to create a task",
                })

        # Meeting/Schedule intents
        if any(word in msg for word in ["meeting", "schedule", "calendar", "appointment", "call"]):
            intents.append({
                "tool_name": "schedule_meeting",
                "confidence": 0.85,
                "parameters": self._extract_meeting_params(message),
                "reasoning": "User wants to schedule a meeting",
            })

        # Document intents
        if any(word in msg for word in ["document", "file", "search", "find document", "knowledge", "policy"]):
            if any(word in msg for word in ["question", "what", "how", "why", "explain"]):
                intents.append({
                    "tool_name": "answer_from_docs",
                    "confidence": 0.8,
                    "parameters": {"question": message},
                    "reasoning": "User asking a question about company docs",
                })
            else:
                intents.append({
                    "tool_name": "search_documents",
                    "confidence": 0.8,
                    "parameters": {"query": message},
                    "reasoning": "User wants to search documents",
                })

        if not intents:
            # If no specific intent found, treat as general chat
            return {
                "is_general_chat": True,
                "chat_response": f"I understood your message, but I'm not sure which action to take. Could you be more specific? For example:\n\n• \"Send an email to Taskeen about the API integration\"\n• \"Create a quotation for 5 software licenses for Systems Ltd\"\n• \"Schedule a meeting on Friday after Jummah\"\n• \"Create a task to review the Q3 report\"",
                "intents": [],
                "requires_clarification": False,
            }

        return {
            "intents": intents,
            "requires_clarification": False,
            "is_general_chat": False,
        }

    # --- Parameter Extraction Helpers ---
    # NOTE: These helpers receive the ORIGINAL message (with original casing)
    #       so that regex patterns for capitalized names can work correctly.

    def _extract_name(self, message: str) -> str:
        """Extract a person or company name from the message (original casing)."""
        # Look for capitalized words after prepositions
        patterns = [
            r"(?:to|for|from|about|with)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
            r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",  # Multi-word capitalized (e.g., "CodeCelix")
        ]
        
        stop_words = {
            "the", "a", "an", "my", "our", "this", "that", "send", "create",
            "email", "quotation", "quote", "meeting", "task", "invoice",
            "draft", "schedule", "set", "find", "search", "customer",
            "remind", "reminder", "about", "please", "can", "could",
            "would", "will", "shall", "should", "hello", "hi", "hey",
        }
        
        for pattern in patterns:
            match = re.search(pattern, message)
            if match:
                name = match.group(1).strip()
                if name.lower() not in stop_words and len(name) > 1:
                    return name
        
        # Fallback: try to extract email address as identifier
        email_match = re.search(r'[\w.+-]+@[\w-]+\.[\w.]+', message)
        if email_match:
            return email_match.group(0)
        
        return "Customer"

    def _extract_email_address(self, message: str) -> str:
        """Extract an email address from the message, or generate one from the name."""
        email_match = re.search(r'[\w.+-]+@[\w-]+\.[\w.]+', message)
        if email_match:
            return email_match.group(0)
        
        name = self._extract_name(message)
        if name and name != "Customer":
            return f"{name.lower().replace(' ', '.')}@company.com"
        return ""

    def _extract_email_params(self, message: str) -> dict:
        """Extract email parameters from message (original casing)."""
        to = self._extract_email_address(message)
        name = self._extract_name(message)
        
        # If we found an email use it, otherwise use the name
        recipient = to if to else name
        
        return {
            "to": recipient,
            "subject": "Re: Your Request",
            "body": message,
        }

    def _extract_quotation_params(self, message: str) -> dict:
        """Extract quotation parameters from message (original casing)."""
        name = self._extract_name(message)
        
        # Try to find items and quantities  
        items_match = re.search(r'(\d+)\s+([\w\s]+?)(?:\s+(?:at|for|@)\s+\$?([\d,.]+))?', message, re.IGNORECASE)
        items = message if not items_match else items_match.group(0)

        return {
            "customer_name": name,
            "items": items,
            "notes": "",
        }

    def _extract_invoice_params(self, message: str) -> dict:
        """Extract invoice parameters from message (original casing)."""
        return {
            "customer_name": self._extract_name(message),
            "items": message,
        }

    def _extract_task_params(self, message: str) -> dict:
        """Extract task parameters from message (original casing)."""
        return {
            "title": message[:100],
            "description": message,
            "priority": "medium",
            "deadline": self._extract_time(message.lower()),
        }

    def _extract_meeting_params(self, message: str) -> dict:
        """Extract meeting parameters from message (original casing)."""
        return {
            "title": "Meeting",
            "date": self._extract_time(message.lower()),
            "time": self._extract_clock_time(message),
            "participants": self._extract_name(message),
        }

    def _extract_time(self, msg: str) -> str:
        """Extract time/date references from message (expects lowercased input)."""
        time_patterns = {
            "today": "today",
            "tomorrow": "tomorrow",
            "monday": "Monday",
            "tuesday": "Tuesday",
            "wednesday": "Wednesday",
            "thursday": "Thursday",
            "friday": "Friday",
            "saturday": "Saturday",
            "sunday": "Sunday",
            "next week": "next week",
            "end of day": "end of day",
        }
        for pattern, value in time_patterns.items():
            if pattern in msg:
                return value
        
        # Try "in N days" pattern
        days_match = re.search(r'in\s+(\d+)\s+days?', msg)
        if days_match:
            return f"in {days_match.group(1)} days"
        
        # Try ISO date pattern
        date_match = re.search(r'\d{4}-\d{2}-\d{2}', msg)
        if date_match:
            return date_match.group(0)
        
        return "this week"

    def _extract_clock_time(self, msg: str) -> str:
        """Extract clock time from message."""
        time_match = re.search(r'(\d{1,2})\s*(?::(\d{2}))?\s*(am|pm|AM|PM)', msg)
        if time_match:
            return time_match.group(0)
        time_24 = re.search(r'(\d{1,2}):(\d{2})', msg)
        if time_24:
            return time_24.group(0)
        return "10:00 AM"

    async def _generate_response(self, user_message: str, actions: list, ai_employee_name: str, conversation_id: str) -> str:
        """Generate a human-readable response summarizing the actions taken"""
        if not actions:
            return "I couldn't find any actions to perform. Could you please try rephrasing your request?"

        if self.model:
            return await self._generate_response_ai(user_message, actions, ai_employee_name, conversation_id)

        # Rule-based response generation
        successful = [a for a in actions if a["status"] == "success"]
        failed = [a for a in actions if a["status"] == "error"]

        parts = []
        if successful:
            if len(successful) == 1:
                parts.append(f"Done! {successful[0]['message']}")
            else:
                parts.append(f"I completed {len(successful)} actions:\n")
                for action in successful:
                    parts.append(f"• {action['message']}")

        if failed:
            parts.append(f"\n⚠️ {len(failed)} action(s) had issues:")
            for action in failed:
                parts.append(f"• {action['message']}")

        return "\n".join(parts)

    async def _generate_response_ai(self, user_message: str, actions: list, ai_employee_name: str, conversation_id: str) -> str:
        """Use Groq to generate a natural response — non-blocking async call"""
        try:
            context = conversation_memory.get_context(conversation_id, last_n=3)
            actions_summary = json.dumps(actions, indent=2, default=str)

            prompt = f"""You are {ai_employee_name} for AI Employee OS. The user asked: "{user_message}"

You executed these actions:
{actions_summary}

Generate a brief, professional response summarizing what was done. Be concise. Use bullet points for multiple actions. Include key details like IDs, amounts, dates.
Do not repeat the user's request. Just confirm what was accomplished."""

            # Use async version to avoid blocking the event loop
            response = await self.model.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=settings.AI_MODEL,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.warning("⚠️ AI response generation failed: %s", e)
            # Fallback to rule-based
            parts = []
            for action in actions:
                parts.append(f"• {action['message']}")
            return "Here's what I did:\n" + "\n".join(parts)


# Global agent instance
agent_engine = AgentEngine()
