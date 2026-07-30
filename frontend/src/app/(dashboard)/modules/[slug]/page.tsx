"use client";

import TopBar from "@/components/layout/TopBar";
import { usePathname } from "next/navigation";

export default function ModulePlaceholderPage() {
  const pathname = usePathname();
  const moduleName = pathname.split("/").pop() || "Module";
  
  // Format the name nicely (e.g., "crm" -> "CRM", "email" -> "Email")
  const formattedName = moduleName === "crm" 
    ? "CRM" 
    : moduleName.charAt(0).toUpperCase() + moduleName.slice(1);
    
  let owner = "a teammate";
  if (moduleName === "email") owner = "Taskeen Mustafa";
  if (moduleName === "crm") owner = "Faez Ahmad";
  if (moduleName === "quotations") owner = "Hassan Raza";
  if (moduleName === "documents") owner = "Absar Akbar";
  if (moduleName === "tasks") owner = "Ali Zafar";

  return (
    <>
      <TopBar title={`${formattedName} Module`} subtitle={`Assigned to ${owner}`} />
      
      <div style={{ padding: "40px 32px", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", minHeight: "calc(100vh - 140px)" }}>
        <div style={{ fontSize: 64, marginBottom: 24, animation: "float 3s ease-in-out infinite" }}>
          🚧
        </div>
        
        <h2 style={{ fontSize: 24, fontWeight: 700, color: "var(--text-primary)", marginBottom: 12 }}>
          {formattedName} Module Under Construction
        </h2>
        
        <p style={{ fontSize: 15, color: "var(--text-secondary)", textAlign: "center", maxWidth: 500, lineHeight: 1.6, marginBottom: 32 }}>
          This module is currently being developed by <strong>{owner}</strong> as part of the team task division. 
          Once completed, it will be integrated here into the main AI Employee OS platform.
        </p>
        
        <div className="glass-card" style={{ padding: 24, width: "100%", maxWidth: 600 }}>
          <h3 style={{ fontSize: 14, fontWeight: 600, color: "var(--text-primary)", marginBottom: 16 }}>
            Integration Status
          </h3>
          
          <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <div style={{ width: 24, height: 24, borderRadius: "50%", background: "var(--success)", display: "flex", alignItems: "center", justifyContent: "center", color: "white", fontSize: 12 }}>✓</div>
              <p style={{ fontSize: 14, color: "var(--text-primary)" }}>UI Shell & Navigation created</p>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <div style={{ width: 24, height: 24, borderRadius: "50%", background: "var(--success)", display: "flex", alignItems: "center", justifyContent: "center", color: "white", fontSize: 12 }}>✓</div>
              <p style={{ fontSize: 14, color: "var(--text-primary)" }}>Tool interface protocol defined</p>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <div style={{ width: 24, height: 24, borderRadius: "50%", background: "var(--success)", display: "flex", alignItems: "center", justifyContent: "center", color: "white", fontSize: 12 }}>✓</div>
              <p style={{ fontSize: 14, color: "var(--text-primary)" }}>AI Agent stubs implemented</p>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <div style={{ width: 24, height: 24, borderRadius: "50%", border: "2px solid var(--border-secondary)", display: "flex", alignItems: "center", justifyContent: "center", color: "var(--text-muted)", fontSize: 12 }}>○</div>
              <p style={{ fontSize: 14, color: "var(--text-secondary)" }}>Waiting for {owner} to complete the UI and API endpoints</p>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <div style={{ width: 24, height: 24, borderRadius: "50%", border: "2px solid var(--border-secondary)", display: "flex", alignItems: "center", justifyContent: "center", color: "var(--text-muted)", fontSize: 12 }}>○</div>
              <p style={{ fontSize: 14, color: "var(--text-secondary)" }}>Swap AI agent stubs with real implementation</p>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
