"use client";

import { useState, useEffect } from "react";
import TopBar from "@/components/layout/TopBar";

interface Report {
  id: number;
  title: string;
  report_type: string;
  data: any;
  created_at: string;
}

export default function ReportsPage() {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [formData, setFormData] = useState({ title: "", report_type: "sales", summary: "" });

  const fetchReports = () => {
    fetch("http://localhost:8000/api/reports")
      .then((res) => res.json())
      .then((data) => {
        setReports(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch reports", err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchReports();
  }, []);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/api/reports", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: formData.title,
          report_type: formData.report_type,
          data: { summary: formData.summary }
        })
      });
      if (res.ok) {
        setIsGenerating(false);
        setFormData({ title: "", report_type: "sales", summary: "" });
        fetchReports();
      }
    } catch (error) {
      console.error("Failed to generate report", error);
    }
  };

  return (
    <>
      <TopBar title="Reports" subtitle="Analytics & Insights" />
      <div style={{ padding: 32 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
          <h2 style={{ fontSize: 24, fontWeight: 600 }}>Analytics Reports</h2>
          <button className="primary-button" onClick={() => setIsGenerating(true)}>Generate Report</button>
        </div>

        {isGenerating && (
          <div style={{
            position: "fixed", top: 0, left: 0, right: 0, bottom: 0, 
            backgroundColor: "rgba(0,0,0,0.5)", zIndex: 100,
            display: "flex", alignItems: "center", justifyContent: "center"
          }}>
            <div className="glass-card" style={{ padding: 24, width: 450, backgroundColor: "var(--bg-secondary)" }}>
              <h3 style={{ marginBottom: 16, fontSize: 18, fontWeight: 600 }}>Generate Report</h3>
              <form onSubmit={handleGenerate} style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                <input 
                  required
                  type="text" 
                  placeholder="Report Title"
                  value={formData.title}
                  onChange={(e) => setFormData({...formData, title: e.target.value})}
                  className="chat-input"
                  style={{ border: "1px solid var(--border-primary)" }}
                />
                <select 
                  value={formData.report_type}
                  onChange={(e) => setFormData({...formData, report_type: e.target.value})}
                  className="chat-input"
                  style={{ border: "1px solid var(--border-primary)", backgroundColor: "var(--bg-primary)" }}
                >
                  <option value="sales">Sales Report</option>
                  <option value="expense">Expense Report</option>
                  <option value="performance">Performance Report</option>
                </select>
                <textarea 
                  required
                  placeholder="Summary/Content..."
                  value={formData.summary}
                  onChange={(e) => setFormData({...formData, summary: e.target.value})}
                  className="chat-input"
                  style={{ minHeight: 120, border: "1px solid var(--border-primary)", resize: "vertical" }}
                />
                <div style={{ display: "flex", gap: 12, justifyContent: "flex-end", marginTop: 8 }}>
                  <button type="button" className="btn-secondary" onClick={() => setIsGenerating(false)}>Cancel</button>
                  <button type="submit" className="primary-button">Generate</button>
                </div>
              </form>
            </div>
          </div>
        )}

        <div className="glass-card" style={{ padding: 24 }}>
          {loading ? (
            <p>Loading reports...</p>
          ) : reports.length === 0 ? (
            <div style={{ textAlign: "center", padding: "40px 0", color: "var(--text-muted)" }}>
              <p>No reports found.</p>
              <p style={{ fontSize: 12 }}>Try asking the AI Assistant to generate a sales or expense report!</p>
            </div>
          ) : (
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: 24 }}>
              {reports.map((r) => (
                <div key={r.id} style={{ padding: 20, border: "1px solid var(--border-secondary)", borderRadius: 12, background: "var(--bg-secondary)" }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 16 }}>
                    <h3 style={{ fontSize: 18, fontWeight: 600 }}>{r.title}</h3>
                    <span className="badge badge-accent" style={{ textTransform: "capitalize" }}>{r.report_type}</span>
                  </div>
                  <div style={{ fontSize: 14, color: "var(--text-secondary)", marginBottom: 16 }}>
                    {r.data?.summary || "No summary available for this report."}
                  </div>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", fontSize: 12, color: "var(--text-muted)", borderTop: "1px solid var(--border-secondary)", paddingTop: 12 }}>
                    <span>ID: #{r.id}</span>
                    <span>{new Date(r.created_at).toLocaleDateString()}</span>
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
