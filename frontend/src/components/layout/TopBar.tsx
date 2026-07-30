"use client";

interface TopBarProps {
  title?: string;
  subtitle?: string;
}

export default function TopBar({ title, subtitle }: TopBarProps) {
  return (
    <header
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "16px 32px",
        borderBottom: "1px solid var(--border-secondary)",
        background: "rgba(10, 10, 15, 0.8)",
        backdropFilter: "blur(20px)",
        position: "sticky",
        top: 0,
        zIndex: 30,
      }}
    >
      {/* Left: Page Title */}
      <div>
        {title && (
          <h2
            style={{ fontSize: 20, fontWeight: 700, color: "var(--text-primary)" }}
          >
            {title}
          </h2>
        )}
        {subtitle && (
          <p
            style={{
              fontSize: 13,
              color: "var(--text-muted)",
              marginTop: 2,
            }}
          >
            {subtitle}
          </p>
        )}
      </div>

      {/* Right: Actions */}
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        {/* Search */}
        <div style={{ position: "relative" }}>
          <input
            type="text"
            placeholder="Search anything..."
            className="input-field"
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                alert(`Search for "${e.currentTarget.value}" coming soon!`);
              }
            }}
            style={{
              width: 240,
              paddingLeft: 36,
              fontSize: 13,
              padding: "8px 12px 8px 36px",
              borderRadius: 8,
            }}
          />
          <span
            style={{
              position: "absolute",
              left: 12,
              top: "50%",
              transform: "translateY(-50%)",
              fontSize: 14,
              opacity: 0.4,
            }}
          >
            🔍
          </span>
        </div>

        {/* Notifications */}
        <button
          onClick={() => alert("No new notifications")}
          style={{
            width: 36,
            height: 36,
            borderRadius: 8,
            background: "var(--bg-tertiary)",
            border: "1px solid var(--border-secondary)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            cursor: "pointer",
            fontSize: 16,
            position: "relative",
          }}
        >
          🔔
        </button>

        {/* User Avatar */}
        <div
          onClick={() => alert("Profile menu (coming soon)")}
          style={{
            display: "flex",
            alignItems: "center",
            gap: 10,
            padding: "4px 12px 4px 4px",
            borderRadius: 10,
            background: "var(--bg-tertiary)",
            border: "1px solid var(--border-secondary)",
            cursor: "pointer",
          }}
        >
          <div
            style={{
              width: 28,
              height: 28,
              borderRadius: 7,
              background: "var(--accent-gradient)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 13,
              fontWeight: 700,
              color: "white",
            }}
          >
            MA
          </div>
          <span style={{ fontSize: 13, fontWeight: 500 }}>Muhammad Awais</span>
        </div>
      </div>
    </header>
  );
}
