# Installation Guide (fresh computer)

You need: Python 3.11+, Node.js 18+ (LTS), Git, and VS Code. Commands marked **PowerShell** are for Windows; **Terminal** is macOS/Linux.

## 1. Install prerequisites
| Tool | Where | Verify |
|---|---|---|
| Python 3.11+ | https://www.python.org/downloads/ (Windows: tick **Add python.exe to PATH**) | `python --version` (macOS/Linux: `python3 --version`) |
| Node.js LTS (includes npm) | https://nodejs.org | `node -v` and `npm -v` |
| Git | https://git-scm.com/downloads | `git --version` |
| VS Code | https://code.visualstudio.com | open it, then **View > Terminal** |
| GitHub account | https://github.com/signup | (needed later) |

Close and reopen the terminal after installing so PATH updates apply.

## 2. Open the project
Unzip `PATHFINDER.zip`, then in VS Code choose **File > Open Folder** and select the `PATHFINDER` folder. Open two terminals (**Terminal > New Terminal**, then the split icon).

## 3. Backend (terminal 1)
**PowerShell**
```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```
**Terminal (macOS/Linux)**
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
Check: open http://127.0.0.1:8000/docs. You should see the Swagger page, and http://127.0.0.1:8000/api/health returns `{"status":"ok"}`.

Run the tests (new terminal, venv active, inside `backend`): `python -m pytest -v` (expect 21 passed).

## 4. Frontend (terminal 2)
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173. Keep both terminals running.

### How they connect
In development Vite proxies `/api/...` to `http://127.0.0.1:8000` (see `frontend/vite.config.js`), so no CORS or URL setup is needed. To point at a different backend, create `frontend/.env.local` with `VITE_API_BASE_URL=http://127.0.0.1:8000` and restart `npm run dev`. The backend then allows `http://localhost:5173` by default; add other origins with the `ALLOWED_ORIGINS` environment variable.

## 5. Production build check
```bash
cd frontend
npm run build
```
## Troubleshooting
| Problem | Fix |
|---|---|
| PowerShell: "running scripts is disabled" when activating | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, reopen the terminal, activate again. |
| `python` / `pip` not found | Reinstall Python with "Add to PATH"; on Windows try `py -m venv .venv`; on macOS/Linux use `python3`/`pip3`. |
| `uvicorn: command not found` | The virtual environment is not active. Activate it (prompt shows `(.venv)`) and rerun `pip install -r requirements.txt`. |
| `ModuleNotFoundError: algorithms` | Run uvicorn and pytest from inside the `backend` folder. |
| Port 8000 or 5173 in use | Use `uvicorn main:app --port 8001`, and set `target` in `vite.config.js` to match. |
| Page says "Cannot reach the PATHFINDER backend" | Backend not running, or wrong `VITE_API_BASE_URL`. Check http://127.0.0.1:8000/api/health. |
| Browser console: CORS error | Add your frontend origin to `ALLOWED_ORIGINS` (exact scheme, host and port, no trailing slash) and restart the backend. |
| `npm install` fails | Check `node -v` is 18 or newer; delete `node_modules` and retry. |
| Fonts look different offline | The app falls back to system fonts; Google Fonts load only online. |
