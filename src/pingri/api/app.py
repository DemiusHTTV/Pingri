import os

from fastapi import Depends, FastAPI, Request

from pingri.api.events import router as events_router
from pingri.api.overview import router as overview_router
from pingri.api.people import router as people_router
from pingri.api.security import check_api_key, check_chief_key
from pingri.api.store import store
from pingri.api.tasks import router as tasks_router

app = FastAPI(title="Pingri API", version="0.1.0")


@app.middleware("http")
async def load_local_mocks(request: Request, call_next):
    worker_env = request.scope.get("env")
    enabled = getattr(worker_env, "LOAD_MOCK_DATA", None) or os.getenv("LOAD_MOCK_DATA")
    if str(enabled).lower() in {"1", "true", "yes"}:
        store.load_mock_data()
    return await call_next(request)


app.include_router(events_router, dependencies=[Depends(check_api_key)])
app.include_router(overview_router, dependencies=[Depends(check_chief_key)])
app.include_router(tasks_router, dependencies=[Depends(check_api_key)])
app.include_router(people_router, dependencies=[Depends(check_api_key)])


@app.get("/", tags=["Сервис"])
async def root() -> dict[str, str]:
    return {
        "service": "Pingri API",
        "status": "ok",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", tags=["Сервис"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
