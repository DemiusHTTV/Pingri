import hmac
import os

from fastapi import HTTPException, Request


async def check_api_key(request: Request) -> None:
    await _check_key(request, "API_KEY", "X-API-Key")


async def check_chief_key(request: Request) -> None:
    await _check_key(request, "CHIEF_API_KEY", "X-Chief-Key")


async def _check_key(request: Request, name: str, header: str) -> None:
    worker_env = request.scope.get("env")
    expected = getattr(worker_env, name, None) or os.getenv(name)
    supplied = request.headers.get(header)
    if not expected:
        raise HTTPException(status_code=503, detail=f"{name} не настроен")
    if not supplied or not hmac.compare_digest(supplied, expected):
        raise HTTPException(status_code=401, detail="Нет доступа")
