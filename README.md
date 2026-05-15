# HMCTS task manager (technical exercise)

For this challenge, I chose to use languages and tools I am trying to be more comfortable with, while keeping the design close to the kind of full-stack service HMCTS described. Although the workplace stack may use different technologies such as Java, Spring Boot, Node.js, Azure, Docker, and Kubernetes, this project helped me show that the underlying principles are transferable. I focused on building a clean REST API, validating input, handling errors, storing data in a database, documenting endpoints with Swagger/OpenAPI, and connecting the frontend to the backend. This helped me practise solving the same engineering problems that appear across different languages: clear structure, maintainable code, testing, reliable data handling, and building software around user needs.

Caseworkers manage **tasks** with a **Flask + SQLite** API and a **React (Vite)** UI: create, list, update **status**, and delete tasks.

## Repository layout

- **`backend/`** — REST API, validation (Marshmallow), OpenAPI + Swagger UI, pytest.
- **`frontend/`** — Single-page app; in dev, Vite proxies `/api` to the API.

## Prerequisites

- **Python 3.12** (recommended; also works on **3.11** and **3.13**). Avoid relying on **3.14-only** installs on machines that only have older Pythons — use 3.12 from [python.org](https://www.python.org/downloads/) or **pyenv** / **uv**.
- **Node.js 20+** and npm (see `frontend/.nvmrc`).

## Portable backend setup (avoid `pip install` / version errors)

Use a **fixed Python version** before creating the venv. **`backend/.python-version`** is set to **`3.12`** for [pyenv](https://github.com/pyenv/pyenv) users.

### macOS / Linux

```bash
cd backend

# 1) Use Python 3.12.x (pick ONE approach)

# A — pyenv (recommended if you use it)
pyenv install 3.12.8 --skip-existing   # or any 3.12.x
pyenv local 3.12.8                     # reads .python-version; optional if file already says 3.12
python3 --version                      # should show 3.12.x

# B — python.org installer: ensure `python3.12` is on PATH, then:
# python3.12 -m venv venv

# 2) Create venv with THAT interpreter only
python3 -m venv venv
./venv/bin/python -V                   # confirm 3.12.x inside venv

# 3) Modern pip + wheel (fixes many “could not build wheel” errors)
./venv/bin/python -m pip install --upgrade pip setuptools wheel

# 4) Install project deps
./venv/bin/pip install -r requirements.txt

# 5) Verify
./venv/bin/pytest -q
```

### Windows (PowerShell)

```powershell
cd backend

# Use Python 3.12 from Microsoft Store or python.org; then:
py -3.12 -m venv venv
.\venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
.\venv\Scripts\pip.exe install -r requirements.txt
.\venv\Scripts\pytest.exe -q
```

### If `pip install` still fails

1. Paste the **full error** (often mentions missing **Visual C++ Build Tools** on Windows, or **OpenSSL** on old Linux).
2. Try a **clean venv**: delete the `venv` folder, recreate from step 2.
3. Ensure you are **not** mixing `pip` from the system with the venv — always **`./venv/bin/pip`** (or `.\venv\Scripts\pip.exe`).

### Run the API

```bash
cd backend
PORT=5001 ./venv/bin/python run.py
```

- API base: `http://127.0.0.1:5001`
- **Swagger UI:** `http://127.0.0.1:5001/docs`
- **OpenAPI JSON:** `http://127.0.0.1:5001/openapi.json`
- SQLite file: **`backend/tasks.db`** (created on first run; delete to reset the DB)

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
