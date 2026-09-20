@echo off
cd /d "%~dp0backend"
if not exist ".env" (
  copy ".env.example" ".env" >nul
  echo Created backend\.env from .env.example.
  echo Edit backend\.env with your MySQL password and optional AI settings.
)
python -m uvicorn main:app --reload
pause
