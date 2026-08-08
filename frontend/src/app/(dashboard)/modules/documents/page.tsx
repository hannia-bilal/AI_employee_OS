"use client";

import { useState, useEffect } from "react";
import TopBar from "@/components/layout/TopBar";

interface Document {
  id: number;
  title: string;
  content: string;
  author: string;
  document_type: string;
  created_at: string;
}

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [isUploading, setIsUploading] = useState(false);
  const [formData, setFormData] = useState({ title: "", content: "", author: "", document_type: "note" });

  const fetchDocuments = () => {
    fetch("http://localhost:8000/api/documents")
      .then((res) => res.json())
      .then((data) => {
        setDocuments(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch documents", err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/api/documents", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });
      if (res.ok) {
        setIsUploading(false);
        setFormData({ title: "", content: "", author: "", document_type: "note" });
        fetchDocuments();
      }
    } catch (error) {
      console.error("Failed to upload document", error);
    }
  };

  return (
    <>
      <TopBar title="Documents" subtitle="Knowledge Base" />
      <div style={{ padding: 32 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
          <h2 style={{ fontSize: 24, fontWeight: 600 }}>Knowledge Base</h2>
          <button className="primary-button" onClick={() => setIsUploading(true)}>Upload Document</button>
        </div>

        {isUploading && (
          <div style={{
            position: "fixed", top: 0, left: 0, right: 0, bottom: 0, 
            backgroundColor: "rgba(0,0,0,0.5)", zIndex: 100,
            display: "flex", alignItems: "center", justifyContent: "center"
          }}>
            <div className="glass-card" style={{ padding: 24, width: 500, backgroundColor: "var(--bg-secondary)" }}>
              <h3 style={{ marginBottom: 16, fontSize: 18, fontWeight: 600 }}>Upload Document</h3>
              <form onSubmit={handleUpload} style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                <input 
                  required
                  type="text" 
                  placeholder="Document Title"
                  value={formData.title}
                  onChange={(e) => setFormData({...formData, title: e.target.value})}
                  className="chat-input"
                  style={{ border: "1px solid var(--border-primary)" }}
                />
                <input 
                  required
                  type="text" 
                  placeholder="Author"
                  value={formData.author}
                  onChange={(e) => setFormData({...formData, author: e.target.value})}
                  className="chat-input"
                  style={{ border: "1px solid var(--border-primary)" }}
                />
                <select 
                  value={formData.document_type}
                  onChange={(e) => setFormData({...formData, document_type: e.target.value})}
                  className="chat-input"
                  style={{ border: "1px solid var(--border-primary)", backgroundColor: "var(--bg-primary)" }}
                >
                  <option value="note">Note</option>
                  <option value="pdf">PDF (Text representation)</option>
                  <option value="docx">DOCX (Text representation)</option>
                </select>
                <textarea 
                  required
                  placeholder="Document Content..."
                  value={formData.content}
                  onChange={(e) => setFormData({...formData, content: e.target.value})}
                  className="chat-input"
                  style={{ minHeight: 150, border: "1px solid var(--border-primary)", resize: "vertical" }}
                />
                <div style={{ display: "flex", gap: 12, justifyContent: "flex-end", marginTop: 8 }}>
                  <button type="button" className="btn-secondary" onClick={() => setIsUploading(false)}>Cancel</button>
                  <button type="submit" className="primary-button">Upload</button>
                </div>
              </form>
            </div>
          </div>
        )}

        <div className="glass-card" style={{ padding: 24 }}>
          {loading ? (
            <p>Loading documents...</p>
          ) : documents.length === 0 ? (
            <div style={{ textAlign: "center", padding: "40px 0", color: "var(--text-muted)" }}>
              <p>No documents found.</p>
              <p style={{ fontSize: 12 }}>Currently you need to add documents to the database to see them here.</p>
            </div>
          ) : (
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr))", gap: 24 }}>
              {documents.map((d) => (
                <div key={d.id} style={{ padding: 16, border: "1px solid var(--border-secondary)", borderRadius: 12, background: "var(--bg-secondary)" }}>
                  <div style={{ fontSize: 24, marginBottom: 12 }}>
                    {d.document_type === "pdf" ? "📄" : d.document_type === "docx" ? "📝" : "🗒️"}
                  </div>
                  <h3 style={{ fontSize: 16, fontWeight: 600, marginBottom: 8 }}>{d.title}</h3>
                  <p style={{ fontSize: 13, color: "var(--text-secondary)", marginBottom: 12, height: 40, overflow: "hidden" }}>
                    {d.content.substring(0, 80)}...
                  </p>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", fontSize: 11, color: "var(--text-muted)" }}>
                    <span>{d.author || "Unknown"}</span>
                    <span>{new Date(d.created_at).toLocaleDateString()}</span>
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
