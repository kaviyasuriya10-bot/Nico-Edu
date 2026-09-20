# NicoEdu — AI-Powered Student Study System

NicoEdu is a full-stack student study system built with **FastAPI, MySQL, HTML, CSS and vanilla JavaScript**.

## Included features

- Student registration and login
- JWT authentication with bcrypt password hashing
- Subjects and topics with progress
- Personal notes
- Quiz creation and attempts
- Study goals
- Progress dashboard and activity history
- Admin dashboard
- Optional AI tutor
- Responsive frontend

## Important: do not share secrets

The original uploaded project contained a `backend/.env` file with a database password and an AI API key. Those secrets have **not** been included in this cleaned ZIP.

If that API key is real, rotate/revoke it in the provider dashboard before using the project again.

## Requirements

- Python 3.11+ recommended
- MySQL 5.5+ (MySQL 8.0+ recommended)
- A modern browser

## 1. Create the database

Open MySQL and run:

```sql
SOURCE backend/database/schema.sql;
```

Or from a terminal:

```bash
mysql -u root -p < backend/database/schema.sql
```

## 2. Configure the backend

Copy:

```text
backend/.env.example
```

to:

```text
backend/.env
```

Then edit the values, especially:

```env
DATABASE_PASSWORD=YOUR_MYSQL_PASSWORD
SECRET_KEY=CHANGE_THIS_TO_A_LONG_RANDOM_SECRET
```

AI is optional. Leave `AI_PROVIDER`, `AI_API_KEY`, and `AI_MODEL` blank if you do not want AI features.

## 3. Install Python packages

Windows:

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r backend\requirements.txt
```

Then start the API:

```bat
cd backend
python -m uvicorn main:app --reload
```

API:
`http://127.0.0.1:8000`

Swagger docs:
`http://127.0.0.1:8000/docs`

## 4. Start the frontend

Open a second terminal in the project folder:

```bat
python -m http.server 5500 --directory frontend
```

Open:

`http://127.0.0.1:5500`

You can also double-click `START_BACKEND.bat` and `START_FRONTEND.bat`.

## 5. Create an admin

Register a normal account first, then run in MySQL:

```sql
UPDATE nicoedu.users
SET role='admin'
WHERE username='your-admin-username';
```

## Project structure

```text
NicoEdu/
├── backend/
│   ├── api/
│   ├── database/
│   ├── models/
│   ├── services/
│   ├── utils/
│   ├── .env.example
│   ├── config.py
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── *.html
│   ├── css/
│   └── js/
├── tests/
├── START_BACKEND.bat
├── START_FRONTEND.bat
└── README.md
```

## Validation

From the project root:

```bash
python -m compileall backend
pytest -q
```

The project ZIP intentionally does **not** contain a Python virtual environment, cache files, API keys, or database passwords. Install dependencies locally with `pip install -r backend/requirements.txt`.
