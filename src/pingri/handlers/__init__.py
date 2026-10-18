from aiogram import Router

from pingri.handlers import common
from pingri.handlers import events
from pingri.handlers import task
from pingri.handlers import admin
from pingri.handlers import directory

def build_router() -> Router:
    """Собирает все роутеры. Порядок важен: апдейт уходит в первый
    подошедший хэндлер и дальше не передаётся."""
    router = Router()
    router.include_router(common.router)
    router.include_router(events.router)
    router.include_router(task.router)
    router.include_router(admin.router)
    router.include_router(directory.router)
    return router
