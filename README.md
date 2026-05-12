# HMCTS task manager (technical exercise)

Caseworkers manage **tasks** with a **Flask + SQLite** API and a **React (Vite)** UI: create, list, update **status**, and delete tasks.

## Repository layout

- **`backend/`** — REST API, validation (Marshmallow), OpenAPI + Swagger UI, pytest.
- **`frontend/`** — Single-page app; in dev, Vite proxies `/api` to the API.

## Prerequisites

- Python **3.12+** (project tested with 3.14)
- **Node.js 20+** and npm

## Backend

```bash
cd backend
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
./venv/bin/pytest -q
PORT=5001 ./venv/bin/python run.py
```

- API base: `http://127.0.0.1:5001`
- **Swagger UI:** `http://127.0.0.1:5001/docs`
- **OpenAPI JSON:** `http://127.0.0.1:5001/openapi.json`
- SQLite file: `backend/tasks.db` (delete the file if you change the schema and need a clean DB)

Optional: `DATABASE_URL=postgresql+psycopg://...` if you switch the app to Postgres (requires installing a driver and updating the URI).

## Frontend

In another terminal (with the API already running on port **5001**):

```bash
cd frontend
npm install
npm run dev
```

Open **http://127.0.0.1:5173**. The dev server proxies `/api`, `/openapi.json`, and `/docs` to **`http://127.0.0.1:5001`** (see `frontend/vite.config.ts`). If you run the API on another port, update the proxy `target` there.

Production build:

```bash
cd frontend
npm run build
```

Serve the contents of `frontend/dist/` with any static host, and set **`VITE_API_URL`** at build time to your public API origin if the UI and API are on different hosts (e.g. `VITE_API_URL=https://api.example.com`).

## API summary

| Method | Path | Description |
|--------|------|--------------|
| GET | `/api/tasks` | List all tasks |
| POST | `/api/tasks` | Create (`title`, optional `description`, `status`, `due_date` ISO) |
| GET | `/api/tasks/<id>` | Get one task |
| PATCH | `/api/tasks/<id>` | Update `status` only |
| DELETE | `/api/tasks/<id>` | Delete |

Allowed `status` values: `pending`, `in_progress`, `completed`, `cancelled`.

## Licence

Use for assessment / learning as appropriate.
