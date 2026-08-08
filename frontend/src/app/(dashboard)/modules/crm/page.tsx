"use client";

import { useState, useEffect } from "react";
import TopBar from "@/components/layout/TopBar";

interface Customer {
  id: string;
  name: string;
  email: string;
  company: string;
  phone: string;
  status: string;
  pipeline_stage: string;
  total_revenue: number;
}

export default function CRMPage() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const [isAdding, setIsAdding] = useState(false);
  const [formData, setFormData] = useState({ name: "", email: "", company: "", phone: "", pipeline_stage: "lead" });

  const fetchCustomers = () => {
    fetch("http://localhost:8000/api/crm/customers")
      .then((res) => res.json())
      .then((data) => {
        setCustomers(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch customers", err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchCustomers();
  }, []);

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/api/crm/customers", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({...formData, status: "active", total_revenue: 0})
      });
      if (res.ok) {
        setIsAdding(false);
        setFormData({ name: "", email: "", company: "", phone: "", pipeline_stage: "lead" });
        fetchCustomers();
      }
    } catch (error) {
      console.error("Failed to add customer", error);
    }
  };

  return (
    <>
      <TopBar title="CRM" subtitle="Customer Relationship Management" />
      <div style={{ padding: 32 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
          <h2 style={{ fontSize: 24, fontWeight: 600 }}>Customers & Leads</h2>
          <button className="primary-button" onClick={() => setIsAdding(true)}>Add Customer</button>
        </div>

        {isAdding && (
          <div style={{
            position: "fixed", top: 0, left: 0, right: 0, bottom: 0, 
            backgroundColor: "rgba(0,0,0,0.5)", zIndex: 100,
            display: "flex", alignItems: "center", justifyContent: "center"
          }}>
            <div className="glass-card" style={{ padding: 24, width: 450, backgroundColor: "var(--bg-secondary)" }}>
              <h3 style={{ marginBottom: 16, fontSize: 18, fontWeight: 600 }}>Add Customer</h3>
              <form onSubmit={handleAdd} style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                <input 
                  required
                  type="text" 
                  placeholder="Full Name"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  className="chat-input"
                  style={{ border: "1px solid var(--border-primary)" }}
                />
                <input 
                  type="email" 
                  placeholder="Email Address"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  className="chat-input"
                  style={{ border: "1px solid var(--border-primary)" }}
                />
                <input 
                  type="text" 
                  placeholder="Company"
                  value={formData.company}
                  onChange={(e) => setFormData({...formData, company: e.target.value})}
                  className="chat-input"
                  style={{ border: "1px solid var(--border-primary)" }}
                />
                <input 
                  type="text" 
                  placeholder="Phone"
                  value={formData.phone}
                  onChange={(e) => setFormData({...formData, phone: e.target.value})}
                  className="chat-input"
                  style={{ border: "1px solid var(--border-primary)" }}
                />
                <select 
                  value={formData.pipeline_stage}
                  onChange={(e) => setFormData({...formData, pipeline_stage: e.target.value})}
                  className="chat-input"
                  style={{ border: "1px solid var(--border-primary)", backgroundColor: "var(--bg-primary)" }}
                >
                  <option value="lead">Lead</option>
                  <option value="contacted">Contacted</option>
                  <option value="qualified">Qualified</option>
                  <option value="proposal">Proposal</option>
                  <option value="won">Won</option>
                </select>
                <div style={{ display: "flex", gap: 12, justifyContent: "flex-end", marginTop: 8 }}>
                  <button type="button" className="btn-secondary" onClick={() => setIsAdding(false)}>Cancel</button>
                  <button type="submit" className="primary-button">Save</button>
                </div>
              </form>
            </div>
          </div>
        )}

        <div className="glass-card" style={{ padding: 24 }}>
          {loading ? (
            <p>Loading customers...</p>
          ) : customers.length === 0 ? (
            <div style={{ textAlign: "center", padding: "40px 0", color: "var(--text-muted)" }}>
              <p>No customers found.</p>
              <p style={{ fontSize: 12 }}>Try adding one through the AI Assistant!</p>
            </div>
          ) : (
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr style={{ borderBottom: "1px solid var(--border-secondary)", textAlign: "left" }}>
                  <th style={{ padding: 12, fontWeight: 600, color: "var(--text-secondary)" }}>Name</th>
                  <th style={{ padding: 12, fontWeight: 600, color: "var(--text-secondary)" }}>Company</th>
                  <th style={{ padding: 12, fontWeight: 600, color: "var(--text-secondary)" }}>Email</th>
                  <th style={{ padding: 12, fontWeight: 600, color: "var(--text-secondary)" }}>Stage</th>
                </tr>
              </thead>
              <tbody>
                {customers.map((c) => (
                  <tr key={c.id} style={{ borderBottom: "1px solid var(--border-secondary)" }}>
                    <td style={{ padding: 12, fontWeight: 500 }}>{c.name}</td>
                    <td style={{ padding: 12, color: "var(--text-secondary)" }}>{c.company || "-"}</td>
                    <td style={{ padding: 12, color: "var(--text-secondary)" }}>{c.email || "-"}</td>
                    <td style={{ padding: 12 }}>
                      <span className="badge badge-accent">{c.pipeline_stage}</span>
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
