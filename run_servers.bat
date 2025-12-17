@echo off
setlocal enabledelayedexpansion

echo.
echo ============================================================
echo    SignVerse AI - Starting Servers
echo ============================================================
echo.

REM Get current directory
set SCRIPT_DIR=%CD%

REM Start Backend in a new window
echo Starting Backend Server on port 8000...
start "Backend Server" cmd /k "cd %SCRIPT_DIR%\backend && .\venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
echo ✓ Backend starting...

REM Wait a bit
timeout /t 2 /nobreak

REM Start ML Server in a new window
echo Starting ML Server on port 8001...
start "ML Server" cmd /k "cd %SCRIPT_DIR%\ml_server && .\venv_infer\Scripts\python -m uvicorn main:app --host 0.0.0.0 --port 8001"
echo ✓ ML Server starting...

echo.
echo ============================================================
echo Both servers are starting in separate windows...
echo ============================================================
echo.
echo ✓ Backend:   http://localhost:8000
echo ✓ ML Server: http://localhost:8001
echo.
