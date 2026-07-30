"use client";

import TopBar from "@/components/layout/TopBar";
import { useState, useEffect } from "react";

interface DashboardData {
  stats: {
    actions_today: number;
    actions_change: string;
    active_conversations: number;
    conversations_change: string;
    tasks_completed: number;
    tasks_change: string;
    revenue_pipeline: string;
    revenue_change: string;
  };
  recent_activities: Array<{
    id: string;
    type: string;
    description: string;
    timestamp: string;
    status: string;
    icon: string;
  }>;
  ai_insights: Array<{
    icon: string;
    text: string;
    type: string;
  }>;
  ai_employees: Array<{
    name: string;
    avatar: string;
    status: string;
    actions: number;
  }>;
}

export default function DashboardPage() {
  const [loaded, setLoaded] = useState(false);
  const [data, setData] = useState<DashboardData | null>(null);

  useEffect(() => {
    let isMounted = true;
    
    const fetchData = () => {
      fetch("http://localhost:8000/api/dashboard")
        .then((res) => res.json())
        .then((json) => {
          if (isMounted) {
            setData(json);
            setLoaded(true);
          }
        })
        .catch((err) => {
          console.error("Failed to load dashboard data", err);
          if (isMounted) setLoaded(true);
        });
    };

    fetchData(); // Fetch immediately
    
    // Poll every 3 seconds for real-time updates
    const intervalId = setInterval(fetchData, 3000);

    return () => {
      isMounted = false;
      clearInterval(intervalId);
    };
  }, []);

  const kpiCards = data ? [
    {
      label: "AI Actions Today",
      value: data.stats.actions_today.toString(),
      change: data.stats.actions_change,
      icon: "⚡",
      color: "#6366f1",
    },
    {
      label: "Active Conversations",
      value: data.stats.active_conversations.toString(),
      change: data.stats.conversations_change,
      icon: "💬",
      color: "#8b5cf6",
    },
    {
      label: "Tasks Completed",
      value: data.stats.tasks_completed.toString(),
      change: data.stats.tasks_change,
      icon: "✅",
      color: "#22c55e",
    },
    {
      label: "Revenue Pipeline",
      value: data.stats.revenue_pipeline,
      change: data.stats.revenue_change,
      icon: "💰",
      color: "#f59e0b",
    },
  ] : [
    { label: "AI Actions Today", value: "-", change: "", icon: "⚡", color: "#6366f1" },
    { label: "Active Conversations", value: "-", change: "", icon: "💬", color: "#8b5cf6" },
    { label: "Tasks Completed", value: "-", change: "", icon: "✅", color: "#22c55e" },
    { label: "Revenue Pipeline", value: "-", change: "", icon: "💰", color: "#f59e0b" },
  ];

  const recentActivities = data?.recent_activities || [];
  const aiInsights = data?.ai_insights || [];
  const aiEmployees = data?.ai_employees || [];

  return (
    <>
      <TopBar title="Dashboard" subtitle="Welcome back, Muhammad Awais" />

      <div style={{ padding: "24px 32px" }}>
        {/* KPI Cards */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
            gap: 20,
            marginBottom: 28,
          }}
        >
          {kpiCards.map((card, i) => (
            <div
              key={card.label}
              className={`kpi-card ${loaded ? "animate-slide-in-up" : ""}`}
              style={{
                opacity: loaded ? 1 : 0,
                animationDelay: `${i * 0.08}s`,
              }}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "flex-start",
                  marginBottom: 16,
                }}
              >
                <span
                  style={{
                    fontSize: 12,
                    fontWeight: 600,
                    color: "var(--text-secondary)",
                    textTransform: "uppercase",
                    letterSpacing: "0.05em",
                  }}
                >
                  {card.label}
                </span>
                <div
                  style={{
                    width: 40,
                    height: 40,
                    borderRadius: 10,
                    background: `${card.color}15`,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 20,
                  }}
                >
                  {card.icon}
                </div>
              </div>
              <div style={{ display: "flex", alignItems: "baseline", gap: 10 }}>
                <span
                  style={{
                    fontSize: 32,
                    fontWeight: 800,
                    color: "var(--text-primary)",
                    lineHeight: 1,
                  }}
                >
                  {card.value}
                </span>
                <span
                  style={{
                    fontSize: 13,
                    fontWeight: 600,
                    color: card.change.startsWith("+")
                      ? "var(--success)"
                      : "var(--error)",
                  }}
                >
                  {card.change}
                </span>
              </div>
            </div>
          ))}
        </div>

        {/* Main Grid */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 380px",
            gap: 20,
          }}
        >
          {/* Left Column */}
          <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
            {/* Recent Activity */}
            <div className="glass-card" style={{ padding: 24 }}>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  marginBottom: 20,
                }}
              >
                <h3
                  style={{
                    fontSize: 16,
                    fontWeight: 700,
                    color: "var(--text-primary)",
                  }}
                >
                  Recent Activity
                </h3>
                <span className="badge badge-accent">Live</span>
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: 2 }}>
                {recentActivities.map((activity) => (
                  <div
                    key={activity.id}
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: 12,
                      padding: "12px 0",
                      borderBottom: "1px solid var(--border-secondary)",
                    }}
                  >
                    <span style={{ fontSize: 18, flexShrink: 0 }}>
                      {activity.icon}
                    </span>
                    <p
                      style={{
                        flex: 1,
                        fontSize: 13,
                        color: "var(--text-secondary)",
                        lineHeight: 1.5,
                      }}
                    >
                      {activity.text}
                    </p>
                    <span
                      style={{
                        fontSize: 11,
                        color: "var(--text-muted)",
                        whiteSpace: "nowrap",
                      }}
                    >
                      {activity.time}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* AI Employees Grid */}
            <div className="glass-card" style={{ padding: 24 }}>
              <h3
                style={{
                  fontSize: 16,
                  fontWeight: 700,
                  color: "var(--text-primary)",
                  marginBottom: 16,
                }}
              >
                AI Employees
              </h3>
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(3, 1fr)",
                  gap: 12,
                }}
              >
                {aiEmployees.map((emp) => (
                  <div
                    key={emp.name}
                    style={{
                      padding: 16,
                      borderRadius: 12,
                      background: "var(--bg-tertiary)",
                      border: "1px solid var(--border-secondary)",
                      textAlign: "center",
                      cursor: "pointer",
                      transition: "all 0.2s ease",
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.borderColor =
                        "var(--border-primary)";
                      e.currentTarget.style.transform = "translateY(-2px)";
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.borderColor =
                        "var(--border-secondary)";
                      e.currentTarget.style.transform = "translateY(0)";
                    }}
                  >
                    <div style={{ fontSize: 28, marginBottom: 8 }}>
                      {emp.avatar}
                    </div>
                    <p
                      style={{
                        fontSize: 12,
                        fontWeight: 600,
                        color: "var(--text-primary)",
                        marginBottom: 4,
                      }}
                    >
                      {emp.name}
                    </p>
                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        gap: 4,
                      }}
                    >
                      <div
                        style={{
                          width: 6,
                          height: 6,
                          borderRadius: "50%",
                          background:
                            emp.status === "active"
                              ? "var(--success)"
                              : "var(--text-muted)",
                        }}
                      />
                      <span
                        style={{
                          fontSize: 11,
                          color: "var(--text-muted)",
                          textTransform: "capitalize",
                        }}
                      >
                        {emp.status}
                      </span>
                    </div>
                    <p
                      style={{
                        fontSize: 11,
                        color: "var(--text-muted)",
                        marginTop: 6,
                      }}
                    >
                      {emp.actions} actions today
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Column - AI Insights */}
          <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
            <div className="glass-card" style={{ padding: 24 }}>
              <h3
                style={{
                  fontSize: 16,
                  fontWeight: 700,
                  color: "var(--text-primary)",
                  marginBottom: 16,
                  display: "flex",
                  alignItems: "center",
                  gap: 8,
                }}
              >
                <span className="gradient-text">AI Insights</span>
                <span className="animate-float" style={{ fontSize: 18 }}>
                  ✨
                </span>
              </h3>
              <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                {aiInsights.map((insight, i) => (
                  <div
                    key={i}
                    style={{
                      padding: 14,
                      borderRadius: 10,
                      background: "var(--bg-tertiary)",
                      border: "1px solid var(--border-secondary)",
                      display: "flex",
                      gap: 10,
                      alignItems: "flex-start",
                      cursor: "pointer",
                      transition: "all 0.2s ease",
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.borderColor =
                        "var(--border-primary)";
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.borderColor =
                        "var(--border-secondary)";
                    }}
                  >
                    <span style={{ fontSize: 16, flexShrink: 0 }}>
                      {insight.icon}
                    </span>
                    <p
                      style={{
                        fontSize: 13,
                        color: "var(--text-secondary)",
                        lineHeight: 1.5,
                      }}
                    >
                      {insight.text}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Quick Actions */}
            <div className="glass-card" style={{ padding: 24 }}>
              <h3
                style={{
                  fontSize: 16,
                  fontWeight: 700,
                  color: "var(--text-primary)",
                  marginBottom: 16,
                }}
              >
                Quick Actions
              </h3>
              <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                {[
                  { icon: "📧", label: "Draft an email", href: "/command-center" },
                  { icon: "📝", label: "Create quotation", href: "/command-center" },
                  { icon: "✅", label: "Create a task", href: "/command-center" },
                  { icon: "📅", label: "Schedule meeting", href: "/command-center" },
                  { icon: "👤", label: "Find customer", href: "/command-center" },
                ].map((action) => (
                  <a
                    key={action.label}
                    href={action.href}
                    className="sidebar-nav-item"
                    style={{
                      textDecoration: "none",
                      borderRadius: 8,
                      padding: "10px 14px",
                    }}
                  >
                    <span style={{ fontSize: 16 }}>{action.icon}</span>
                    <span style={{ fontSize: 13 }}>{action.label}</span>
                    <span
                      style={{
                        marginLeft: "auto",
                        fontSize: 14,
                        opacity: 0.3,
                      }}
                    >
                      →
                    </span>
                  </a>
                ))}
              </div>
            </div>

            {/* System Status */}
            <div className="glass-card" style={{ padding: 24 }}>
              <h3
                style={{
                  fontSize: 16,
                  fontWeight: 700,
                  color: "var(--text-primary)",
                  marginBottom: 16,
                }}
              >
                System Status
              </h3>
              <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                {[
                  { label: "AI Engine", status: "online", detail: "Rule-based mode" },
                  { label: "Tools", status: "online", detail: "13 registered" },
                  { label: "Database", status: "online", detail: "SQLite" },
                  { label: "API", status: "online", detail: "Port 8000" },
                ].map((item) => (
                  <div
                    key={item.label}
                    style={{
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                    }}
                  >
                    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                      <div
                        style={{
                          width: 8,
                          height: 8,
                          borderRadius: "50%",
                          background:
                            item.status === "online"
                              ? "var(--success)"
                              : "var(--error)",
                        }}
                      />
                      <span style={{ fontSize: 13, fontWeight: 500 }}>
                        {item.label}
                      </span>
                    </div>
                    <span style={{ fontSize: 12, color: "var(--text-muted)" }}>
                      {item.detail}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
