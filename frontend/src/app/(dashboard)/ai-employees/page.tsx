"use client";

import TopBar from "@/components/layout/TopBar";
import { useState, useEffect } from "react";

export default function AIEmployeesPage() {
  const [aiEmployees, setAiEmployees] = useState<any[]>([]);
  const [isHiring, setIsHiring] = useState(false);
  const [formData, setFormData] = useState({ name: "", role: "", description: "" });

  const fetchEmployees = () => {
    fetch("http://localhost:8000/api/ai-employees")
      .then(res => res.json())
      .then(data => setAiEmployees(data))
      .catch(err => console.error("Failed to fetch AI employees", err));
  };

  useEffect(() => {
    fetchEmployees();
  }, []);

  const handleHire = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/api/ai-employees", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: formData.name,
          role: formData.role,
          description: formData.description,
          avatar: "🤖",
          allowed_tools: ["Search Documents", "Send Email"],
          color: "#10b981"
        })
      });
      if (res.ok) {
        setIsHiring(false);
        setFormData({ name: "", role: "", description: "" });
        fetchEmployees();
      }
    } catch (error) {
      console.error("Failed to hire AI", error);
    }
  };

  return (
    <>
      <TopBar title="AI Employees" subtitle="Manage your digital workforce" />
      
      <div style={{ padding: "24px 32px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
          <h2 style={{ fontSize: 18, fontWeight: 700, color: "var(--text-primary)" }}>Active Agents</h2>
          <button className="btn-primary" onClick={() => setIsHiring(true)}>+ Hire New AI</button>
        </div>

        {isHiring && (
          <div style={{
            position: "fixed", top: 0, left: 0, right: 0, bottom: 0, 
            backgroundColor: "rgba(0,0,0,0.5)", zIndex: 100,
            display: "flex", alignItems: "center", justifyContent: "center"
          }}>
            <div className="glass-card" style={{ padding: 24, width: 400, backgroundColor: "var(--bg-secondary)" }}>
              <h3 style={{ marginBottom: 16, fontSize: 18, fontWeight: 600 }}>Hire New AI Employee</h3>
              <form onSubmit={handleHire} style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                <input required type="text" placeholder="Name (e.g. Marketing Manager)" value={formData.name} onChange={(e) => setFormData({...formData, name: e.target.value})} className="chat-input" style={{ border: "1px solid var(--border-primary)" }} />
                <input required type="text" placeholder="Role (e.g. Social Media)" value={formData.role} onChange={(e) => setFormData({...formData, role: e.target.value})} className="chat-input" style={{ border: "1px solid var(--border-primary)" }} />
                <textarea required placeholder="Description of responsibilities..." value={formData.description} onChange={(e) => setFormData({...formData, description: e.target.value})} className="chat-input" style={{ minHeight: 80, border: "1px solid var(--border-primary)", resize: "vertical" }} />
                <div style={{ display: "flex", gap: 12, justifyContent: "flex-end", marginTop: 8 }}>
                  <button type="button" className="btn-secondary" onClick={() => setIsHiring(false)}>Cancel</button>
                  <button type="submit" className="primary-button">Hire AI</button>
                </div>
              </form>
            </div>
          </div>
        )}

        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))", gap: 24 }}>
          {aiEmployees.map((agent) => (
            <div key={agent.id} className="glass-card" style={{ padding: 24, display: "flex", flexDirection: "column" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 16 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
                  <div style={{ width: 56, height: 56, borderRadius: 16, background: `${agent.color}15`, border: `1px solid ${agent.color}30`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 28 }}>
                    {agent.avatar}
                  </div>
                  <div>
                    <h3 style={{ fontSize: 16, fontWeight: 700, color: "var(--text-primary)" }}>{agent.name}</h3>
                    <p style={{ fontSize: 13, color: "var(--text-muted)", marginTop: 2 }}>{agent.role}</p>
                  </div>
                </div>
                <div style={{ width: 8, height: 8, borderRadius: "50%", background: agent.is_active ? "var(--success)" : "var(--text-muted)" }} title={agent.is_active ? "active" : "idle"} />
              </div>
              
              <p style={{ fontSize: 13, color: "var(--text-secondary)", lineHeight: 1.5, marginBottom: 20, flex: 1 }}>
                {agent.description}
              </p>
              
              <div style={{ borderTop: "1px solid var(--border-secondary)", paddingTop: 16 }}>
                <p style={{ fontSize: 11, fontWeight: 600, color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 8 }}>
                  Available Tools
                </p>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                  {agent.allowed_tools && agent.allowed_tools.map((tool: string) => (
                    <span key={tool} className="badge" style={{ background: "var(--bg-tertiary)", border: "1px solid var(--border-secondary)", color: "var(--text-secondary)" }}>
                      {tool}
                    </span>
                  ))}
                </div>
              </div>
              
              <div style={{ display: "flex", gap: 8, marginTop: 20 }}>
                <button className="btn-secondary" style={{ flex: 1, justifyContent: "center", background: "var(--accent-gradient)", color: "white", border: "none" }} onClick={() => window.location.href = `/command-center?persona=${agent.id}`}>
                  Chat with {agent.name.split(' ')[0]}
                </button>
                <button className="btn-secondary" style={{ flex: 1, justifyContent: "center" }}>Configure</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}
