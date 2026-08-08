"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

const navItems = [
  {
    label: "Dashboard",
    href: "/dashboard",
    icon: "📊",
    description: "Overview & insights",
  },
  {
    label: "Command Center",
    href: "/command-center",
    icon: "🤖",
    description: "AI Assistant chat",
  },
  {
    label: "AI Employees",
    href: "/ai-employees",
    icon: "👥",
    description: "Manage AI agents",
  },
  { type: "divider" as const, label: "Modules" },
  {
    label: "Email",
    href: "/modules/email",
    icon: "📧",
    description: "Taskeen's module",
    badge: "Team",
  },
  {
    label: "CRM",
    href: "/modules/crm",
    icon: "👤",
    description: "Faez's module",
    badge: "Team",
  },
  {
    label: "Quotations",
    href: "/modules/quotations",
    icon: "📝",
    description: "Hassan's module",
    badge: "Team",
  },
  {
    label: "Documents",
    href: "/modules/documents",
    icon: "📄",
    description: "Absar's module",
    badge: "Team",
  },
  {
    label: "Tasks",
    href: "/modules/tasks",
    icon: "✅",
    description: "Ali's module",
    badge: "Team",
  },
  {
    label: "WhatsApp",
    href: "/modules/whatsapp",
    icon: "💬",
    description: "WhatsApp Assistant",
    badge: "Team",
  },
  {
    label: "Reports",
    href: "/modules/reports",
    icon: "📈",
    description: "Analytics & Reporting",
    badge: "Team",
  },
];

export default function Sidebar() {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside className={`sidebar ${collapsed ? "collapsed" : ""}`}>
      {/* Logo */}
      <div
        style={{
          padding: "20px 20px 16px",
          borderBottom: "1px solid var(--border-secondary)",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <div
            style={{
              width: 36,
              height: 36,
              borderRadius: 10,
              background: "var(--accent-gradient)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 18,
              flexShrink: 0,
            }}
          >
            🤖
          </div>
          {!collapsed && (
            <div>
              <h1
                style={{
                  fontSize: 16,
                  fontWeight: 700,
                  color: "var(--text-primary)",
                  lineHeight: 1.2,
                }}
              >
                AI Employee<span className="gradient-text"> OS</span>
              </h1>
              <p
                style={{
                  fontSize: 11,
                  color: "var(--text-muted)",
                  marginTop: 2,
                }}
              >
                Digital Workforce
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Navigation */}
      <nav
        style={{
          padding: "12px",
          flex: 1,
          overflowY: "auto",
        }}
      >
        {navItems.map((item, i) => {
          if ("type" in item && item.type === "divider") {
            return !collapsed ? (
              <div
                key={i}
                style={{
                  fontSize: 11,
                  fontWeight: 600,
                  color: "var(--text-muted)",
                  textTransform: "uppercase",
                  letterSpacing: "0.05em",
                  padding: "16px 16px 8px",
                }}
              >
                {item.label}
              </div>
            ) : (
              <div
                key={i}
                style={{
                  height: 1,
                  background: "var(--border-secondary)",
                  margin: "12px 8px",
                }}
              />
            );
          }

          if (!("href" in item)) return null;

          const isActive = pathname === item.href;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`sidebar-nav-item ${isActive ? "active" : ""}`}
              style={{ position: "relative" }}
              title={collapsed ? item.label : undefined}
            >
              <span style={{ fontSize: 18, flexShrink: 0 }}>{item.icon}</span>
              {!collapsed && (
                <>
                  <span style={{ flex: 1 }}>{item.label}</span>
                  {"badge" in item && item.badge && (
                    <span
                      className="badge badge-accent"
                      style={{ fontSize: 10, padding: "2px 6px" }}
                    >
                      {item.badge}
                    </span>
                  )}
                </>
              )}
            </Link>
          );
        })}
      </nav>

      {/* Bottom section */}
      <div
        style={{
          padding: "12px",
          borderTop: "1px solid var(--border-secondary)",
        }}
      >
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="sidebar-nav-item"
          style={{
            width: "100%",
            border: "none",
            background: "none",
            position: "relative",
          }}
        >
          <span style={{ fontSize: 18 }}>{collapsed ? "→" : "←"}</span>
          {!collapsed && <span>Collapse</span>}
        </button>

        {!collapsed && (
          <div
            style={{
              padding: "12px 16px",
              marginTop: 8,
              borderRadius: 12,
              background: "rgba(99, 102, 241, 0.08)",
              border: "1px solid rgba(99, 102, 241, 0.15)",
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
              <div
                style={{
                  width: 8,
                  height: 8,
                  borderRadius: "50%",
                  background: "var(--success)",
                }}
              />
              <span style={{ fontSize: 12, fontWeight: 600 }}>Demo Mode</span>
            </div>
            <p style={{ fontSize: 11, color: "var(--text-muted)", marginBottom: 4 }}>
              Rule-based AI • No API key
            </p>
            <p style={{ fontSize: 10, color: "var(--accent)", fontWeight: 600 }}>
              Built by Muhammad Awais
            </p>
          </div>
        )}
      </div>
    </aside>
  );
}
