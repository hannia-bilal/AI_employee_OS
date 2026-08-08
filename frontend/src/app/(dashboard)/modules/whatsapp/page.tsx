"use client";

import { useState, useEffect } from "react";
import TopBar from "@/components/layout/TopBar";

interface WhatsAppMessage {
  id: number;
  phone_number: string;
  message: string;
  direction: string;
  status: string;
  created_at: string;
}

export default function WhatsAppPage() {
  const [messages, setMessages] = useState<WhatsAppMessage[]>([]);
  const [loading, setLoading] = useState(true);
  const [isComposing, setIsComposing] = useState(false);
  const [formData, setFormData] = useState({ phone_number: "", message: "" });

  const fetchMessages = () => {
    fetch("http://localhost:8000/api/whatsapp")
      .then((res) => res.json())
      .then((data) => {
        setMessages(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch whatsapp messages", err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchMessages();
  }, []);

  const handleCompose = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/api/whatsapp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          phone_number: formData.phone_number,
          message: formData.message,
          direction: "outbound",
          status: "sent"
        })
      });
      if (res.ok) {
        setIsComposing(false);
        setFormData({ phone_number: "", message: "" });
        fetchMessages();
      }
    } catch (error) {
      console.error("Failed to send message", error);
    }
  };

  return (
    <>
      <TopBar title="WhatsApp" subtitle="Conversations & Support" />
      <div style={{ padding: 32 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
          <h2 style={{ fontSize: 24, fontWeight: 600 }}>WhatsApp Messages</h2>
          <button className="primary-button" onClick={() => setIsComposing(true)}>New Message</button>
        </div>

        {isComposing && (
          <div style={{
            position: "fixed", top: 0, left: 0, right: 0, bottom: 0, 
            backgroundColor: "rgba(0,0,0,0.5)", zIndex: 100,
            display: "flex", alignItems: "center", justifyContent: "center"
          }}>
            <div className="glass-card" style={{ padding: 24, width: 400, backgroundColor: "var(--bg-secondary)" }}>
              <h3 style={{ marginBottom: 16, fontSize: 18, fontWeight: 600 }}>New WhatsApp Message</h3>
              <form onSubmit={handleCompose} style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                <input 
                  required
                  type="text" 
                  placeholder="Phone Number (e.g. +1234567890)"
                  value={formData.phone_number}
                  onChange={(e) => setFormData({...formData, phone_number: e.target.value})}
                  className="chat-input"
                  style={{ border: "1px solid var(--border-primary)" }}
                />
                <textarea 
                  required
                  placeholder="Type your message here..."
                  value={formData.message}
                  onChange={(e) => setFormData({...formData, message: e.target.value})}
                  className="chat-input"
                  style={{ minHeight: 100, border: "1px solid var(--border-primary)", resize: "vertical" }}
                />
                <div style={{ display: "flex", gap: 12, justifyContent: "flex-end", marginTop: 8 }}>
                  <button type="button" className="btn-secondary" onClick={() => setIsComposing(false)}>Cancel</button>
                  <button type="submit" className="primary-button">Send Message</button>
                </div>
              </form>
            </div>
          </div>
        )}

        <div className="glass-card" style={{ padding: 24 }}>
          {loading ? (
            <p>Loading messages...</p>
          ) : messages.length === 0 ? (
            <div style={{ textAlign: "center", padding: "40px 0", color: "var(--text-muted)" }}>
              <p>No WhatsApp messages found.</p>
              <p style={{ fontSize: 12 }}>Try asking the AI Assistant to send a WhatsApp message to someone!</p>
            </div>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {messages.map((m) => (
                <div key={m.id} style={{ 
                  padding: 16, 
                  border: "1px solid var(--border-secondary)", 
                  borderRadius: 12,
                  background: m.direction === 'outbound' ? "var(--bg-secondary)" : "transparent",
                  marginLeft: m.direction === 'outbound' ? 'auto' : '0',
                  marginRight: m.direction === 'inbound' ? 'auto' : '0',
                  maxWidth: '80%'
                }}>
                  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
                    <div style={{ fontWeight: 600, color: "var(--accent)" }}>{m.phone_number}</div>
                    <div style={{ fontSize: 11, color: "var(--text-muted)" }}>
                      {new Date(m.created_at).toLocaleString()}
                    </div>
                  </div>
                  <div style={{ fontSize: 14, color: "var(--text-primary)" }}>
                    {m.message}
                  </div>
                  <div style={{ marginTop: 8, textAlign: "right", fontSize: 11, color: "var(--text-secondary)" }}>
                    {m.status} {m.direction === 'outbound' ? '✓' : ''}
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
