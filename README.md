# NicoEdu — AI Powered Student Study System

NicoEdu is a full-stack student study system: subjects, topics, notes, quizzes and attempts, goals, progress tracking, an admin area, and a configurable AI tutor. It is built from scratch with FastAPI, MySQL, HTML/CSS, and vanilla JavaScript.

## Features

- JWT login and registration with bcrypt password hashing and `student` / `admin` roles.
- Per-user ownership checks for subjects, topics, notes, quizzes, results, goals, and AI conversations.
- Subject/topic progress, activity, goals, and quiz scoring.
- AI chat plus summary, notes, question, and quiz generation endpoints, with friendly unavailable-state handling.
- Responsive blue/purple UI, dark mode, landing, student dashboard and admin dashboard.

## Setup

Create the database and tables, then configure the backend:

```bash
mysql -u root -p < backend/database/schema.sql
cp backend/.env.example backend/.env
python -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
cd backend
python -m uvicorn main:app --reload
```

Set a strong unique `SECRET_KEY` and correct MySQL values in `backend/.env`. Serve the frontend separately:

```bash
python -m http.server 5500 --directory frontend
```

Open `http://localhost:5500`. The frontend infers the API URL as `http://localhost:8000/api`; it can be changed from Settings.

To make an admin, register a user, then run:

```sql
UPDATE nicoedu.users SET role='admin' WHERE username='your-admin-username';
```

## AI configuration

The included adapter supports OpenAI. Keep all keys on the backend only:

```env
AI_PROVIDER=openai
AI_API_KEY=your-server-only-key
AI_MODEL=gpt-4o-mini
```

Without these values, the application remains functional and AI requests return a helpful configuration message. Add providers in `backend/services/ai_service.py`.

## Architecture

`backend/api` contains protected FastAPI routes; `database/schema.sql` is the complete MySQL schema; `utils/security.py` handles bcrypt/JWT; `frontend` is a vanilla JS client. FastAPI Swagger documentation is available at `/docs`.

## HTTPS deployment

Place Uvicorn behind Caddy or Nginx, terminate TLS at the proxy, serve `frontend/` as static files, proxy `/api` privately, and set `CORS_ORIGINS` to the public HTTPS origin. Do not expose `.env`, database credentials, or AI keys.

## Validation and troubleshooting

```bash
pytest -q
python -m compileall backend
```

If MySQL cannot connect, check that the server is running and the `.env` credentials match. For CORS errors, add the exact frontend origin to `CORS_ORIGINS`. An unavailable AI message means AI environment variables have not yet been configured.
