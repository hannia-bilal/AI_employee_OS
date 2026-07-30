"use client";

import TopBar from "@/components/layout/TopBar";
import { useState, useRef, useEffect } from "react";
import { api, type ChatResponse, type ActionResult } from "@/lib/api";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  actions?: ActionResult[];
  isLoading?: boolean;
}

const suggestedCommands = [
  "Send a quotation to Faez for 3 custom modules at Rs. 45,000 each",
  "Schedule a meeting on Friday after Jummah with the team",
  "Create a task to prepare the Q3 sales report by Thursday",
  "Find customer CodeCelix and show their details",
  "Draft an email to taskeen.mustafa@codecelix.com about the project update",
  "Set a reminder to follow up with Ali in 3 days",
];

export default function CommandCenterPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      content:
        "Hello! 👋 I'm your AI Executive Assistant. I can help you with:\n\n• 📧 **Emails** — Draft, send, or summarize emails\n• 📝 **Quotations** — Create professional quotations\n• 🧾 **Invoices** — Generate invoices\n• 👤 **CRM** — Find customers, create leads\n• ✅ **Tasks** — Create tasks and set reminders\n• 📅 **Meetings** — Schedule meetings\n• 📄 **Documents** — Search company knowledge base\n\nJust tell me what you need in plain English!",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [backendOnline, setBackendOnline] = useState<boolean | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    // Check if backend is online
    api
      .getHealth()
      .then(() => setBackendOnline(true))
      .catch(() => setBackendOnline(false));
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async (text?: string) => {
    const messageText = text || input.trim();
    if (!messageText || isProcessing) return;

    const userMsg: Message = {
      id: `user-${Date.now()}`,
      role: "user",
      content: messageText,
      timestamp: new Date(),
    };

    const loadingMsg: Message = {
      id: `loading-${Date.now()}`,
      role: "assistant",
      content: "",
      timestamp: new Date(),
      isLoading: true,
    };

    setMessages((prev) => [...prev, userMsg, loadingMsg]);
    setInput("");
    setIsProcessing(true);

    try {
      if (backendOnline) {
        const response: ChatResponse = await api.chat(
          messageText,
          conversationId || undefined
        );

        setConversationId(response.conversation_id);

        const assistantMsg: Message = {
          id: `assistant-${Date.now()}`,
          role: "assistant",
          content: response.response,
          timestamp: new Date(),
          actions: response.actions,
        };

        setMessages((prev) =>
          prev.filter((m) => !m.isLoading).concat(assistantMsg)
        );
      } else {
        // Offline demo mode
        const demoResponse = getDemoResponse(messageText);
        const assistantMsg: Message = {
          id: `assistant-${Date.now()}`,
          role: "assistant",
          content: demoResponse.text,
          timestamp: new Date(),
          actions: demoResponse.actions,
        };

        setTimeout(() => {
          setMessages((prev) =>
            prev.filter((m) => !m.isLoading).concat(assistantMsg)
          );
        }, 800);
      }
    } catch {
      const errorMsg: Message = {
        id: `error-${Date.now()}`,
        role: "assistant",
        content:
          "⚠️ Sorry, I encountered an error processing your request. Please make sure the backend server is running (`uvicorn main:app --reload`) and try again.",
        timestamp: new Date(),
      };
      setMessages((prev) =>
        prev.filter((m) => !m.isLoading).concat(errorMsg)
      );
    } finally {
      setIsProcessing(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <>
      <TopBar
        title="Command Center"
        subtitle="Talk to your AI Executive Assistant"
      />

      <div
        style={{
          display: "flex",
          height: "calc(100vh - 65px)",
        }}
      >
        {/* Chat Area */}
        <div
          style={{
            flex: 1,
            display: "flex",
            flexDirection: "column",
          }}
        >
          {/* Messages */}
          <div
            style={{
              flex: 1,
              overflowY: "auto",
              padding: "24px 32px",
              display: "flex",
              flexDirection: "column",
              gap: 16,
            }}
          >
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`chat-message ${msg.role}`}
                style={{
                  opacity: 0,
                  animation: "fadeIn 0.3s ease-out forwards",
                }}
              >
                {msg.isLoading ? (
                  <div className="typing-indicator">
                    <span />
                    <span />
                    <span />
                  </div>
                ) : (
                  <>
                    {/* Message content */}
                    <div
                      style={{
                        fontSize: 14,
                        lineHeight: 1.7,
                        whiteSpace: "pre-wrap",
                      }}
                      dangerouslySetInnerHTML={{
                        __html: formatMessage(msg.content),
                      }}
                    />

                    {/* Action cards */}
                    {msg.actions && msg.actions.length > 0 && (
                      <div
                        style={{
                          marginTop: 12,
                          display: "flex",
                          flexDirection: "column",
                          gap: 8,
                        }}
                      >
                        {msg.actions.map((action, i) => (
                          <div
                            key={i}
                            style={{
                              padding: 12,
                              borderRadius: 10,
                              background: "rgba(0,0,0,0.2)",
                              border: `1px solid ${
                                action.status === "success"
                                  ? "rgba(34, 197, 94, 0.2)"
                                  : "rgba(239, 68, 68, 0.2)"
                              }`,
                            }}
                          >
                            <div
                              style={{
                                display: "flex",
                                alignItems: "center",
                                gap: 8,
                                marginBottom: 4,
                              }}
                            >
                              <span
                                style={{
                                  fontSize: 12,
                                  fontWeight: 600,
                                  color:
                                    action.status === "success"
                                      ? "var(--success)"
                                      : "var(--error)",
                                }}
                              >
                                {action.status === "success" ? "✅" : "❌"}{" "}
                                {action.tool_name}
                              </span>
                              {action.execution_time_ms && (
                                <span
                                  style={{
                                    fontSize: 10,
                                    color: "var(--text-muted)",
                                    marginLeft: "auto",
                                  }}
                                >
                                  {action.execution_time_ms.toFixed(0)}ms
                                </span>
                              )}
                            </div>
                            <p
                              style={{
                                fontSize: 12,
                                color: "var(--text-secondary)",
                              }}
                            >
                              {action.message}
                            </p>
                          </div>
                        ))}
                      </div>
                    )}
                  </>
                )}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Suggested Commands (shown when few messages) */}
          {messages.length <= 2 && (
            <div
              style={{
                padding: "0 32px 12px",
                display: "flex",
                flexWrap: "wrap",
                gap: 8,
              }}
            >
              {suggestedCommands.map((cmd) => (
                <button
                  key={cmd}
                  onClick={() => sendMessage(cmd)}
                  style={{
                    padding: "8px 14px",
                    borderRadius: 20,
                    background: "var(--bg-tertiary)",
                    border: "1px solid var(--border-secondary)",
                    color: "var(--text-secondary)",
                    fontSize: 12,
                    cursor: "pointer",
                    transition: "all 0.2s ease",
                    fontFamily: "'Inter', sans-serif",
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.borderColor = "var(--accent-primary)";
                    e.currentTarget.style.color = "var(--accent-primary)";
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.borderColor =
                      "var(--border-secondary)";
                    e.currentTarget.style.color = "var(--text-secondary)";
                  }}
                >
                  {cmd}
                </button>
              ))}
            </div>
          )}

          {/* Input Area */}
          <div
            style={{
              padding: "16px 32px 24px",
              borderTop: "1px solid var(--border-secondary)",
            }}
          >
            {/* Backend status */}
            {backendOnline === false && (
              <div
                style={{
                  padding: "8px 14px",
                  borderRadius: 8,
                  background: "rgba(245, 158, 11, 0.1)",
                  border: "1px solid rgba(245, 158, 11, 0.2)",
                  color: "var(--warning)",
                  fontSize: 12,
                  marginBottom: 12,
                  display: "flex",
                  alignItems: "center",
                  gap: 8,
                }}
              >
                <span>⚠️</span>
                <span>
                  Backend offline — running in demo mode. Start the backend with{" "}
                  <code
                    style={{
                      background: "rgba(0,0,0,0.3)",
                      padding: "2px 6px",
                      borderRadius: 4,
                    }}
                  >
                    uvicorn main:app --reload
                  </code>
                </span>
              </div>
            )}

            <div style={{ display: "flex", gap: 12 }}>
              <input
                ref={inputRef}
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type a command... e.g., 'Send a quotation to John for 25 laptops'"
                className="input-field"
                disabled={isProcessing}
                style={{
                  flex: 1,
                  padding: "14px 18px",
                  fontSize: 14,
                  borderRadius: 12,
                }}
              />
              <button
                onClick={() => sendMessage()}
                disabled={isProcessing || !input.trim()}
                className="btn-primary"
                style={{
                  padding: "14px 28px",
                  borderRadius: 12,
                  opacity: isProcessing || !input.trim() ? 0.5 : 1,
                }}
              >
                {isProcessing ? "⏳" : "🚀"} Send
              </button>
            </div>
          </div>
        </div>

        {/* Right Panel - Action Trace */}
        <div
          style={{
            width: 320,
            borderLeft: "1px solid var(--border-secondary)",
            background: "var(--bg-secondary)",
            padding: 20,
            overflowY: "auto",
          }}
        >
          <h3
            style={{
              fontSize: 14,
              fontWeight: 700,
              color: "var(--text-primary)",
              marginBottom: 16,
              display: "flex",
              alignItems: "center",
              gap: 8,
            }}
          >
            ⚡ Action Trace
          </h3>

          {/* Show actions from all messages */}
          {messages
            .filter((m) => m.actions && m.actions.length > 0)
            .reverse()
            .slice(0, 10)
            .map((msg) => (
              <div key={msg.id} style={{ marginBottom: 16 }}>
                <p
                  style={{
                    fontSize: 11,
                    color: "var(--text-muted)",
                    marginBottom: 8,
                  }}
                >
                  {msg.timestamp.toLocaleTimeString()}
                </p>
                {msg.actions?.map((action, i) => (
                  <div key={i} className="action-trace-step">
                    <div
                      className={`dot ${action.status === "success" ? "success" : "error"}`}
                    />
                    <div>
                      <p
                        style={{
                          fontSize: 12,
                          fontWeight: 600,
                          color: "var(--text-primary)",
                          marginBottom: 2,
                        }}
                      >
                        {action.tool_name.replace(/_/g, " ")}
                      </p>
                      <p
                        style={{
                          fontSize: 11,
                          color: "var(--text-muted)",
                        }}
                      >
                        {action.message}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            ))}

          {!messages.some((m) => m.actions && m.actions.length > 0) && (
            <div
              style={{
                textAlign: "center",
                padding: "40px 20px",
                color: "var(--text-muted)",
              }}
            >
              <p style={{ fontSize: 32, marginBottom: 12 }}>🔍</p>
              <p style={{ fontSize: 13 }}>
                Action trace will appear here when you send commands to the AI
                assistant.
              </p>
            </div>
          )}
        </div>
      </div>
    </>
  );
}

function formatMessage(content: string): string {
  // Convert markdown-like bold to HTML
  let formatted = content.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
  // Convert bullet points
  formatted = formatted.replace(/^• /gm, "• ");
  return formatted;
}

function getDemoResponse(message: string): {
  text: string;
  actions: ActionResult[];
} {
  const msg = message.toLowerCase();

  if (msg.includes("quotation") || msg.includes("quote")) {
    return {
      text: 'Done! I\'ve created a quotation for the requested items.\n\n📝 **Quotation Q-20260729-001** has been generated and is ready for review.',
      actions: [
        {
          tool_name: "create_quotation",
          status: "success",
          message: "📝 Quotation Q-20260729-001 created — Total: Rs. 135,000.00",
          execution_time_ms: 120,
        },
      ],
    };
  }

  if (msg.includes("email") || msg.includes("mail")) {
    return {
      text: "Done! The email has been drafted and is ready to send.",
      actions: [
        {
          tool_name: "send_email",
          status: "success",
          message: '✅ Email sent: "Re: Your Request"',
          execution_time_ms: 85,
        },
      ],
    };
  }

  if (msg.includes("meeting") || msg.includes("schedule")) {
    return {
      text: "Done! Meeting has been scheduled and calendar invites sent.",
      actions: [
        {
          tool_name: "schedule_meeting",
          status: "success",
          message: '📅 Meeting scheduled: "Meeting" on Friday at 3 PM',
          execution_time_ms: 95,
        },
      ],
    };
  }

  if (msg.includes("task") || msg.includes("todo")) {
    return {
      text: "Done! Task has been created and added to your task board.",
      actions: [
        {
          tool_name: "create_task",
          status: "success",
          message: '✅ Task created: "' + message.slice(0, 50) + '"',
          execution_time_ms: 65,
        },
      ],
    };
  }

  if (msg.includes("customer") || msg.includes("find")) {
    return {
      text: "Found the customer! Here are their details:\n\n👤 **CodeCelix**\nEmail: faez.ahmad@codecelix.com\nPipeline: Negotiation\nRevenue: Rs. 4,500,000",
      actions: [
        {
          tool_name: "find_customer",
          status: "success",
          message: '👤 Found customer matching the search',
          execution_time_ms: 45,
        },
      ],
    };
  }

  if (msg.includes("remind")) {
    return {
      text: "Done! Reminder has been set.",
      actions: [
        {
          tool_name: "set_reminder",
          status: "success",
          message: '⏰ Reminder set: "' + message.slice(0, 40) + '"',
          execution_time_ms: 30,
        },
      ],
    };
  }

  return {
    text: "I understood your message, but I'm running in demo mode right now. Start the backend server to get full AI-powered responses!\n\nHere are some things you can try:\n• \"Send a quotation to Faez for 3 custom modules\"\n• \"Schedule a meeting on Friday after Jummah\"\n• \"Create a task to review the Q3 report\"",
    actions: [],
  };
}
