@echo off
:: Planner Auto-Start Script
:: This runs on Windows startup and launches the full Planner stack

:: Start Docker Desktop if not running
tasklist /FI "IMAGENAME eq Docker Desktop.exe" | find /I "Docker Desktop.exe" >nul 2>&1
if errorlevel 1 (
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    timeout /t 30 /nobreak >nul
)

:: Wait for Docker daemon
:wait_docker
"C:\Program Files\Docker\Docker\resources\bin\docker.exe" info >nul 2>&1
if errorlevel 1 (
    timeout /t 5 /nobreak >nul
    goto wait_docker
)

:: Start Postgres
cd /d "C:\Users\HP\Desktop\MTP\Planner"
"C:\Program Files\Docker\Docker\resources\bin\docker.exe" compose up -d

:: Wait for Postgres to be ready
timeout /t 5 /nobreak >nul

:: Start Backend (hidden window)
start /min "Planner Backend" cmd /c "cd /d C:\Users\HP\Desktop\MTP\Planner\backend && .venv\Scripts\python.exe -m uvicorn app.main:app --port 8000"

:: Start Frontend (hidden window)
start /min "Planner Frontend" cmd /c "cd /d C:\Users\HP\Desktop\MTP\Planner\frontend && npm run dev"

:: Wait a moment then open browser
timeout /t 5 /nobreak >nul
start http://localhost:5173
