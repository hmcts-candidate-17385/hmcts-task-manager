import { useCallback, useEffect, useState } from "react";
import {
  createTask,
  deleteTask,
  listTasks,
  patchTaskStatus,
  type Task,
} from "./api";

const STATUSES = [
  "pending",
  "in_progress",
  "completed",
  "cancelled",
] as const;

function formatWhen(iso: string): string {
  try {
    return new Date(iso).toLocaleString(undefined, {
      dateStyle: "medium",
      timeStyle: "short",
    });
  } catch {
    return iso;
  }
}

export default function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [status, setStatus] = useState<string>("pending");
  const [dueLocal, setDueLocal] = useState("");

  const refresh = useCallback(async () => {
    setError(null);
    const data = await listTasks();
    setTasks(data);
  }, []);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      setLoading(true);
      try {
        await refresh();
      } catch (e) {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : "Failed to load tasks");
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [refresh]);

  async function onCreate(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    if (!title.trim()) {
      setError("Title is required.");
      return;
    }
    if (!dueLocal) {
      setError("Due date and time are required.");
      return;
    }
    const due_date = new Date(dueLocal).toISOString();
    try {
      await createTask({
        title: title.trim(),
        description: description.trim() || null,
        status,
        due_date,
      });
      setTitle("");
      setDescription("");
      setStatus("pending");
      setDueLocal("");
      await refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Create failed");
    }
  }

  async function onStatusChange(id: number, next: string) {
    setError(null);
    try {
      await patchTaskStatus(id, next);
      await refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Update failed");
    }
  }

  async function onDelete(id: number) {
    if (!window.confirm("Delete this task?")) return;
    setError(null);
    try {
      await deleteTask(id);
      await refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Delete failed");
    }
  }

  return (
    <div className="page">
      <header className="masthead">
        <div className="masthead__inner">
          <h1 className="masthead__title">Caseworker tasks</h1>
          <p className="masthead__lede">
            Create, view, update status, and delete tasks. API docs:{" "}
            <a href="/docs" target="_blank" rel="noreferrer">
              Swagger UI
            </a>
            .
          </p>
        </div>
      </header>

      <main className="main">
        {error ? (
          <div className="banner banner--error" role="alert">
            {error}
          </div>
        ) : null}

        <section className="panel" aria-labelledby="new-task-heading">
          <h2 id="new-task-heading" className="panel__title">
            New task
          </h2>
          <form className="form" onSubmit={onCreate}>
            <div className="form__row">
              <label htmlFor="title">Title</label>
              <input
                id="title"
                className="input"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                maxLength={120}
                autoComplete="off"
              />
            </div>
            <div className="form__row">
              <label htmlFor="description">Description (optional)</label>
              <textarea
                id="description"
                className="input input--textarea"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={3}
              />
            </div>
            <div className="form__row form__row--split">
              <div>
                <label htmlFor="status">Status</label>
                <select
                  id="status"
                  className="input"
                  value={status}
                  onChange={(e) => setStatus(e.target.value)}
                >
                  {STATUSES.map((s) => (
                    <option key={s} value={s}>
                      {s.replace("_", " ")}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label htmlFor="due">Due date &amp; time</label>
                <input
                  id="due"
                  className="input"
                  type="datetime-local"
                  value={dueLocal}
                  onChange={(e) => setDueLocal(e.target.value)}
                />
              </div>
            </div>
            <div className="form__actions">
              <button type="submit" className="button button--primary">
                Create task
              </button>
            </div>
          </form>
        </section>

        <section className="panel" aria-labelledby="list-heading">
          <h2 id="list-heading" className="panel__title">
            Your tasks
          </h2>
          {loading ? (
            <p className="muted">Loading…</p>
          ) : tasks.length === 0 ? (
            <p className="muted">No tasks yet. Add one above.</p>
          ) : (
            <ul className="task-list">
              {tasks.map((t) => (
                <li key={t.id} className="task-card">
                  <div className="task-card__head">
                    <h3 className="task-card__title">{t.title}</h3>
                    <button
                      type="button"
                      className="button button--warning"
                      onClick={() => onDelete(t.id)}
                    >
                      Delete
                    </button>
                  </div>
                  {t.description ? (
                    <p className="task-card__desc">{t.description}</p>
                  ) : null}
                  <dl className="task-meta">
                    <div>
                      <dt>Due</dt>
                      <dd>{formatWhen(t.due_date)}</dd>
                    </div>
                    <div>
                      <dt>Created</dt>
                      <dd>{formatWhen(t.created_at)}</dd>
                    </div>
                  </dl>
                  <div className="task-card__row">
                    <label htmlFor={`status-${t.id}`} className="task-card__label">
                      Status
                    </label>
                    <select
                      id={`status-${t.id}`}
                      className="input input--inline"
                      value={t.status}
                      onChange={(e) => onStatusChange(t.id, e.target.value)}
                    >
                      {STATUSES.map((s) => (
                        <option key={s} value={s}>
                          {s.replace("_", " ")}
                        </option>
                      ))}
                    </select>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </section>
      </main>

      <footer className="footer">
        <p>HMCTS-style technical exercise — Flask API + React UI.</p>
      </footer>
    </div>
  );
}
