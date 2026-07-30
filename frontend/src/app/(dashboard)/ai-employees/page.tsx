"use client";

import TopBar from "@/components/layout/TopBar";

const aiEmployees = [
  {
    id: 1,
    name: "Executive Assistant",
    role: "System Brain",
    avatar: "🤖",
    description: "The core AI engine that routes requests, understands natural language, and coordinates other specialized agents.",
    tools: ["All Tools"],
    status: "active",
    color: "#6366f1",
  },
  {
    id: 2,
    name: "Sales Manager",
    role: "CRM & Leads",
    avatar: "💼",
    description: "Specializes in managing the sales pipeline, customer relationships, and lead qualification.",
    tools: ["Find Customer", "Create Lead", "Update CRM", "Send Email"],
    status: "active",
    color: "#8b5cf6",
  },
  {
    id: 3,
    name: "Customer Support",
    role: "Support & Docs",
    avatar: "🎧",
    description: "Handles incoming customer queries by searching the knowledge base and drafting helpful responses.",
    tools: ["Search Documents", "Answer from Docs", "Send Email", "Draft Email"],
    status: "active",
    color: "#22c55e",
  },
  {
    id: 4,
    name: "Finance Assistant",
    role: "Billing & Quotes",
    avatar: "💰",
    description: "Manages financial documents including professional quotations, invoices, and payment tracking.",
    tools: ["Create Quotation", "Create Invoice", "Send Email"],
    status: "idle",
    color: "#f59e0b",
  },
  {
    id: 5,
    name: "HR Assistant",
    role: "Internal Tasks",
    avatar: "📋",
    description: "Manages internal tasks, scheduling, employee onboarding documents, and meeting coordination.",
    tools: ["Create Task", "Schedule Meeting", "Set Reminder", "Search Documents"],
    status: "active",
    color: "#ef4444",
  },
];

export default function AIEmployeesPage() {
  return (
    <>
      <TopBar title="AI Employees" subtitle="Manage your digital workforce" />
      
      <div style={{ padding: "24px 32px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
          <h2 style={{ fontSize: 18, fontWeight: 700, color: "var(--text-primary)" }}>Active Agents</h2>
          <button className="btn-primary">+ Hire New AI</button>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))", gap: 24 }}>
          {aiEmployees.map((agent) => (
            <div key={agent.id} className="glass-card" style={{ padding: 24, display: "flex", flexDirection: "column" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 16 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
                  <div style={{
                    width: 56,
                    height: 56,
                    borderRadius: 16,
                    background: `${agent.color}15`,
                    border: `1px solid ${agent.color}30`,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 28,
                  }}>
                    {agent.avatar}
                  </div>
                  <div>
                    <h3 style={{ fontSize: 16, fontWeight: 700, color: "var(--text-primary)" }}>{agent.name}</h3>
                    <p style={{ fontSize: 13, color: "var(--text-muted)", marginTop: 2 }}>{agent.role}</p>
                  </div>
                </div>
                <div style={{
                  width: 8,
                  height: 8,
                  borderRadius: "50%",
                  background: agent.status === "active" ? "var(--success)" : "var(--text-muted)",
                }} title={agent.status} />
              </div>
              
              <p style={{ fontSize: 13, color: "var(--text-secondary)", lineHeight: 1.5, marginBottom: 20, flex: 1 }}>
                {agent.description}
              </p>
              
              <div style={{ borderTop: "1px solid var(--border-secondary)", paddingTop: 16 }}>
                <p style={{ fontSize: 11, fontWeight: 600, color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 8 }}>
                  Available Tools
                </p>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                  {agent.tools.map(tool => (
                    <span key={tool} className="badge" style={{ background: "var(--bg-tertiary)", border: "1px solid var(--border-secondary)", color: "var(--text-secondary)" }}>
                      {tool}
                    </span>
                  ))}
                </div>
              </div>
              
              <div style={{ display: "flex", gap: 8, marginTop: 20 }}>
                <button className="btn-secondary" style={{ flex: 1, justifyContent: "center" }}>Configure</button>
                <button className="btn-secondary" style={{ flex: 1, justifyContent: "center" }}>View Logs</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}
