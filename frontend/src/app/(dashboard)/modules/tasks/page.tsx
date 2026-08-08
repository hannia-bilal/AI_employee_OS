"use client";

import { useState, useEffect } from "react";
import TopBar from "@/components/layout/TopBar";

interface TaskItem {
  id: number;
  title: string;
  description: string;
  assigned_to: string;
  status: string;
  due_date: string;
  created_at: string;
}

export default function TasksPage() {
  const [tasks, setTasks] = useState<TaskItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [isCreating, setIsCreating] = useState(false);
  const [formData, setFormData] = useState({ title: "", description: "", assigned_to: "", status: "todo" });

  const fetchTasks = () => {
    fetch("http://localhost:8000/api/tasks")
      .then((res) => res.json())
      .then((data) => {
        setTasks(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch tasks", err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/api/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });
      if (res.ok) {
        setIsCreating(false);
        setFormData({ title: "", description: "", assigned_to: "", status: "todo" });
        fetchTasks();
      }
    } catch (error) {
      console.error("Failed to create task", error);
    }
  };

  return (
    <>
      <TopBar title="Tasks" subtitle="Task Management" />
      <div style={{ padding: 32 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
          <h2 style={{ fontSize: 24, fontWeight: 600 }}>My Tasks</h2>
          <button className="primary-button" onClick={() => setIsCreating(true)}>New Task</button>
        </div>

        {isCreating && (
          <div style={{
            position: "fixed", top: 0, left: 0, right: 0, bottom: 0, 
            backgroundColor: "rgba(0,0,0,0.5)", zIndex: 100,
            display: "flex", alignItems: "center", justifyContent: "center"
          }}>
            <div className="glass-card" style={{ padding: 24, width: 450, backgroundColor: "var(--bg-secondary)" }}>
              <h3 style={{ marginBottom: 16, fontSize: 18, fontWeight: 600 }}>New Task</h3>
              <form onSubmit={handleCreate} style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                <input 
                  required
                  type="text" 
                  placeholder="Task Title"
                  value={formData.title}
                  onChange={(e) => setFormData({...formData, title: e.target.value})}
                  className="chat-input"
                  style={{ border: "1px solid var(--border-primary)" }}
                />
                <input 
                  type="text" 
                  placeholder="Assigned To"
                  value={formData.assigned_to}
                  onChange={(e) => setFormData({...formData, assigned_to: e.target.value})}
                  className="chat-input"
                  style={{ border: "1px solid var(--border-primary)" }}
                />
                <select 
                  value={formData.status}
                  onChange={(e) => setFormData({...formData, status: e.target.value})}
                  className="chat-input"
                  style={{ border: "1px solid var(--border-primary)", backgroundColor: "var(--bg-primary)" }}
                >
                  <option value="todo">To-Do</option>
                  <option value="in_progress">In Progress</option>
                  <option value="done">Done</option>
                </select>
                <textarea 
                  placeholder="Description..."
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  className="chat-input"
                  style={{ minHeight: 100, border: "1px solid var(--border-primary)", resize: "vertical" }}
                />
                <div style={{ display: "flex", gap: 12, justifyContent: "flex-end", marginTop: 8 }}>
                  <button type="button" className="btn-secondary" onClick={() => setIsCreating(false)}>Cancel</button>
                  <button type="submit" className="primary-button">Create</button>
                </div>
              </form>
            </div>
          </div>
        )}

        <div className="glass-card" style={{ padding: 24 }}>
          {loading ? (
            <p>Loading tasks...</p>
          ) : tasks.length === 0 ? (
            <div style={{ textAlign: "center", padding: "40px 0", color: "var(--text-muted)" }}>
              <p>No tasks found.</p>
              <p style={{ fontSize: 12 }}>Ask the AI Assistant to create a task, schedule a meeting, or set a reminder!</p>
            </div>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {tasks.map((t) => (
                <div key={t.id} style={{ display: "flex", alignItems: "center", gap: 16, padding: 16, border: "1px solid var(--border-secondary)", borderRadius: 8 }}>
                  <div style={{ 
                    width: 20, height: 20, borderRadius: "50%", 
                    border: `2px solid ${t.status === 'todo' ? 'var(--border-secondary)' : t.status === 'scheduled' ? 'var(--accent)' : 'var(--success)'}`,
                    display: "flex", alignItems: "center", justifyContent: "center", fontSize: 10
                  }}>
                    {t.status === 'active' || t.status === 'done' ? "✓" : ""}
                  </div>
                  <div style={{ flex: 1 }}>
                    <h3 style={{ fontSize: 15, fontWeight: 600, color: "var(--text-primary)" }}>{t.title}</h3>
                    {t.description && <p style={{ fontSize: 13, color: "var(--text-secondary)", marginTop: 4, whiteSpace: "pre-line" }}>{t.description}</p>}
                  </div>
                  <div style={{ textAlign: "right" }}>
                    <div style={{ fontSize: 13, fontWeight: 500 }}>{t.assigned_to || "Me"}</div>
                    <div style={{ fontSize: 11, color: "var(--text-muted)", marginTop: 4 }}>
                      {new Date(t.created_at).toLocaleDateString()}
                    </div>
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
