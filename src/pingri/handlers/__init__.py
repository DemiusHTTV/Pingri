from aiogram import Router

from pingri.handlers import common


def build_router() -> Router:
    """Собирает все роутеры. Порядок важен: апдейт уходит в первый
    подошедший хэндлер и дальше не передаётся."""
    router = Router()
    router.include_router(common.router)
    return router
