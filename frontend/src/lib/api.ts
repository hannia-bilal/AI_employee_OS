/**
 * AI Employee OS - API Client
 * Handles all communication with the FastAPI backend
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ActionResult {
  tool_name: string;
  status: string;
  message: string;
  parameters?: Record<string, unknown>;
  result?: Record<string, unknown>;
  execution_time_ms?: number;
}

export interface ChatResponse {
  response: string;
  conversation_id: string;
  actions: ActionResult[];
  intents: Record<string, unknown>[];
  plan: Record<string, unknown>[];
  execution_time_ms: number;
}

export interface DashboardStats {
  total_conversations: number;
  total_actions: number;
  total_tools_used: number;
  active_ai_employees: number;
  actions_today: number;
  success_rate: number;
}

export interface RecentActivity {
  id: string;
  type: string;
  description: string;
  timestamp: string;
  status: string;
}

export interface DashboardData {
  stats: DashboardStats;
  recent_activities: RecentActivity[];
  ai_insights: string[];
}

export interface ToolInfo {
  name: string;
  description: string;
  category: string;
  parameters: Record<string, unknown>;
}

async function apiFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    ...options,
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }

  return res.json();
}

export const api = {
  /** Send a message to the AI assistant */
  chat: (message: string, conversationId?: string, personaId?: number) =>
    apiFetch<ChatResponse>("/api/assistant/chat", {
      method: "POST",
      body: JSON.stringify({
        message,
        conversation_id: conversationId,
        ai_employee_id: personaId ? Number(personaId) : undefined,
      }),
    }),

  /** Get available tools */
  getTools: () =>
    apiFetch<{ tools: ToolInfo[]; total: number }>("/api/assistant/tools"),

  /** Get dashboard data */
  getDashboard: () => apiFetch<DashboardData>("/api/dashboard/"),

  /** Check API health */
  getHealth: () =>
    apiFetch<{
      status: string;
      ai_model: string;
      ai_available: boolean;
      tools_count: number;
      tools: string[];
    }>("/api/assistant/health"),
};
