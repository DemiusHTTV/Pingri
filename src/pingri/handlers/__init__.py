from aiogram import Router

from pingri.handlers import common
from pingri.handlers import events

def build_router() -> Router:
    """Собирает все роутеры. Порядок важен: апдейт уходит в первый
    подошедший хэндлер и дальше не передаётся."""
    router = Router()
    router.include_router(common.router)
    router.include_router(events.router)
    return router
