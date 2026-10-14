import asyncio
import logging


from pingri.handlers import common
from pingri.config import settings
from aiogram import Bot, Dispatcher

dp = Dispatcher()
async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    me = await bot.get_me()
    logging.info("Запущен как @%s", me.username)
    dp.include_router(common.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
