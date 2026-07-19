# dev.ps1 — Windows PowerShell development script
param(
    [Parameter(Position=0)]
    [ValidateSet("dev", "up", "down", "migrate", "seed", "test")]
    [string]$Command = "dev"
)

switch ($Command) {
    "up" {
        docker compose up -d
    }
    "down" {
        docker compose down
    }
    "migrate" {
        Push-Location backend
        alembic upgrade head
        Pop-Location
    }
    "seed" {
        Push-Location backend
        python -m seeds.seed_data
        Pop-Location
    }
    "test" {
        Push-Location backend
        pytest -v
        Pop-Location
    }
    "dev" {
        docker compose up -d
        Write-Host "Starting backend on http://localhost:8000 ..." -ForegroundColor Cyan
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; uvicorn app.main:app --reload --port 8000"
        Write-Host "Starting frontend on http://localhost:5173 ..." -ForegroundColor Cyan
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"
    }
}
