@echo off
setlocal
cd /d "%~dp0backend"

where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install Python 3.12 or newer, then run this file again.
  pause
  exit /b 1
)

if not exist .venv (
  echo Creating Python virtual environment...
  python -m venv .venv
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

cd /d "%~dp0"
if not exist .env (
  copy .env.example .env >nul
  echo.
  echo Created .env from .env.example.
  echo IMPORTANT: Open .env and add SAHMK_API_KEY before testing SAHMK.
  echo.
)

cd /d "%~dp0backend"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
