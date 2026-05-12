/** Base URL for API (empty = same origin, e.g. Vite dev proxy). */
export const apiBase = (): string =>
  (import.meta.env.VITE_API_URL ?? "").replace(/\/$/, "");

async function parseError(res: Response): Promise<string> {
  const text = await res.text();
  try {
    const j = JSON.parse(text) as { message?: string; errors?: unknown };
    if (j.message) return j.message;
    if (j.errors) return JSON.stringify(j.errors);
  } catch {
    /* ignore */
  }
  return text || res.statusText;
}

export type Task = {
  id: number;
  title: string;
  description: string | null;
  status: string;
  due_date: string;
  created_at: string;
  updated_at: string;
};

export type TaskCreate = {
  title: string;
  description?: string | null;
  status: string;
  due_date: string;
};

export async function listTasks(): Promise<Task[]> {
  const r = await fetch(`${apiBase()}/api/tasks`);
  if (!r.ok) throw new Error(await parseError(r));
  return r.json() as Promise<Task[]>;
}

export async function createTask(body: TaskCreate): Promise<Task> {
  const r = await fetch(`${apiBase()}/api/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error(await parseError(r));
  return r.json() as Promise<Task>;
}

export async function patchTaskStatus(
  id: number,
  status: string,
): Promise<Task> {
  const r = await fetch(`${apiBase()}/api/tasks/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  });
  if (!r.ok) throw new Error(await parseError(r));
  return r.json() as Promise<Task>;
}

export async function deleteTask(id: number): Promise<void> {
  const r = await fetch(`${apiBase()}/api/tasks/${id}`, { method: "DELETE" });
  if (!r.ok) throw new Error(await parseError(r));
}
