from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.tasks import router as tasks_router
from app.api.health import router as health_router
from app.api.timetable import router as timetable_router
from app.api.milestones import router as milestones_router
from app.jobs.scheduler import start_scheduler, stop_scheduler
from app.jobs.startup_catchup import run_startup_catchup

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s — %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    start_scheduler()
    run_startup_catchup()  # Catch up on anything missed while laptop was off
    yield
    # Shutdown
    stop_scheduler()


app = FastAPI(
    title="Planner — Personal Command Center",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(timetable_router)
app.include_router(milestones_router)
app.include_router(health_router)
