from datetime import datetime
from zoneinfo import ZoneInfo

from aiogram import F, Router
from aiogram.types import Message

import pingri.texts as txt
from pingri.mock_data import mock_events

router = Router()


async def upcoming_events(days: int = 14) -> list[dict]:
    now = datetime.now(ZoneInfo("Europe/Moscow"))
    until = now.timestamp() + days * 86400
    return [
        event
        for event in mock_events(now)
        if now.timestamp() <= event["starts_at"].timestamp() <= until
    ]


@router.message(F.text == txt.BTN_EVENTS)
async def events(message: Message) -> None:
    items = await upcoming_events(days=14)
    if not items:
        await message.answer("На ближайшие 2 недели мероприятий нет.")
        return

    text = "\n\n".join(
        f"<b>{event['title']}</b>\n{event['starts_at']:%d.%m в %H:%M}"
        for event in items
    )
    await message.answer(f"Ближайшие мероприятия:\n\n{text}")
