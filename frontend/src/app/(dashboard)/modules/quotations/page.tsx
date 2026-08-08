"use client";

import { useState, useEffect } from "react";
import TopBar from "@/components/layout/TopBar";

interface Quotation {
  id: string;
  client_name: string;
  total_amount: number;
  status: string;
  valid_until: string;
}

export default function QuotationsPage() {
  const [quotations, setQuotations] = useState<Quotation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/quotations")
      .then((res) => res.json())
      .then((data) => {
        setQuotations(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch quotations", err);
        setLoading(false);
      });
  }, []);

  return (
    <>
      <TopBar title="Quotations" subtitle="Quotes & Invoices" />
      <div style={{ padding: 32 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
          <h2 style={{ fontSize: 24, fontWeight: 600 }}>Quotations</h2>
          <button className="primary-button">New Quotation</button>
        </div>

        <div className="glass-card" style={{ padding: 24 }}>
          {loading ? (
            <p>Loading quotations...</p>
          ) : quotations.length === 0 ? (
            <div style={{ textAlign: "center", padding: "40px 0", color: "var(--text-muted)" }}>
              <p>No quotations found.</p>
              <p style={{ fontSize: 12 }}>Ask the AI Assistant to generate a quote for a client!</p>
            </div>
          ) : (
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr style={{ borderBottom: "1px solid var(--border-secondary)", textAlign: "left" }}>
                  <th style={{ padding: 12, fontWeight: 600, color: "var(--text-secondary)" }}>ID</th>
                  <th style={{ padding: 12, fontWeight: 600, color: "var(--text-secondary)" }}>Client</th>
                  <th style={{ padding: 12, fontWeight: 600, color: "var(--text-secondary)" }}>Amount</th>
                  <th style={{ padding: 12, fontWeight: 600, color: "var(--text-secondary)" }}>Valid Until</th>
                  <th style={{ padding: 12, fontWeight: 600, color: "var(--text-secondary)" }}>Status</th>
                </tr>
              </thead>
              <tbody>
                {quotations.map((q) => (
                  <tr key={q.id} style={{ borderBottom: "1px solid var(--border-secondary)" }}>
                    <td style={{ padding: 12, fontWeight: 500, fontFamily: "monospace" }}>{q.id}</td>
                    <td style={{ padding: 12, fontWeight: 500 }}>{q.client_name}</td>
                    <td style={{ padding: 12, color: "var(--text-secondary)" }}>Rs. {q.total_amount.toLocaleString()}</td>
                    <td style={{ padding: 12, color: "var(--text-secondary)" }}>{new Date(q.valid_until).toLocaleDateString()}</td>
                    <td style={{ padding: 12 }}>
                      <span className="badge badge-accent">{q.status}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </>
  );
}
