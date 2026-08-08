"use client";

import { useState, useEffect } from "react";
import TopBar from "@/components/layout/TopBar";

interface Email {
  id: number;
  sender: string;
  recipient: string;
  subject: string;
  body: string;
  status: string;
  date: string;
}

export default function EmailPage() {
  const [emails, setEmails] = useState<Email[]>([]);
  const [loading, setLoading] = useState(true);
  const [isComposing, setIsComposing] = useState(false);
  const [formData, setFormData] = useState({ recipient: "", subject: "", body: "" });

  const fetchEmails = () => {
    fetch("http://localhost:8000/api/emails")
      .then((res) => res.json())
      .then((data) => {
        setEmails(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch emails", err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchEmails();
  }, []);

  const handleCompose = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/api/emails", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          sender: "me@company.com", // Mock sender
          recipient: formData.recipient,
          subject: formData.subject,
          body: formData.body,
          status: "sent"
        })
      });
      if (res.ok) {
        setIsComposing(false);
        setFormData({ recipient: "", subject: "", body: "" });
        fetchEmails();
      }
    } catch (error) {
      console.error("Failed to send email", error);
    }
  };

  return (
    <>
      <TopBar title="Email" subtitle="Inbox & Sent Messages" />
      <div style={{ padding: 32 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
          <h2 style={{ fontSize: 24, fontWeight: 600 }}>Emails</h2>
          <button className="primary-button" onClick={() => setIsComposing(true)}>Compose Email</button>
        </div>

        {isComposing && (
          <div style={{
            position: "fixed", top: 0, left: 0, right: 0, bottom: 0, 
            backgroundColor: "rgba(0,0,0,0.5)", zIndex: 100,
            display: "flex", alignItems: "center", justifyContent: "center"
          }}>
            <div className="glass-card" style={{ padding: 24, width: 500, backgroundColor: "var(--bg-secondary)" }}>
              <h3 style={{ marginBottom: 16, fontSize: 18, fontWeight: 600 }}>Compose Email</h3>
              <form onSubmit={handleCompose} style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                <input 
                  required
                  type="email" 
                  placeholder="Recipient (e.g. client@company.com)"
                  value={formData.recipient}
                  onChange={(e) => setFormData({...formData, recipient: e.target.value})}
                  className="chat-input"
                  style={{ border: "1px solid var(--border-primary)" }}
                />
                <input 
                  required
                  type="text" 
                  placeholder="Subject"
                  value={formData.subject}
                  onChange={(e) => setFormData({...formData, subject: e.target.value})}
                  className="chat-input"
                  style={{ border: "1px solid var(--border-primary)" }}
                />
                <textarea 
                  required
                  placeholder="Message body..."
                  value={formData.body}
                  onChange={(e) => setFormData({...formData, body: e.target.value})}
                  className="chat-input"
                  style={{ minHeight: 120, border: "1px solid var(--border-primary)", resize: "vertical" }}
                />
                <div style={{ display: "flex", gap: 12, justifyContent: "flex-end", marginTop: 8 }}>
                  <button type="button" className="btn-secondary" onClick={() => setIsComposing(false)}>Cancel</button>
                  <button type="submit" className="primary-button">Send Email</button>
                </div>
              </form>
            </div>
          </div>
        )}

        <div className="glass-card" style={{ padding: 24 }}>
          {loading ? (
            <p>Loading emails...</p>
          ) : emails.length === 0 ? (
            <div style={{ textAlign: "center", padding: "40px 0", color: "var(--text-muted)" }}>
              <p>No emails found.</p>
              <p style={{ fontSize: 12 }}>Try asking the AI Assistant to draft an email!</p>
            </div>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {emails.map((e) => (
                <div key={e.id} style={{ padding: 16, border: "1px solid var(--border-secondary)", borderRadius: 8 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
                    <div style={{ fontWeight: 600 }}>{e.subject}</div>
                    <div style={{ fontSize: 12, color: "var(--text-muted)" }}>
                      {new Date(e.date).toLocaleDateString()}
                    </div>
                  </div>
                  <div style={{ fontSize: 13, color: "var(--text-secondary)", marginBottom: 8 }}>
                    To: {e.recipient}
                  </div>
                  <div style={{ fontSize: 14, color: "var(--text-primary)" }}>
                    {e.body}
                  </div>
                  <div style={{ marginTop: 12 }}>
                    <span className="badge badge-accent">{e.status}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  );
}
