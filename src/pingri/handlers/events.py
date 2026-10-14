from dataclasses import dataclass
from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.types import Message

import pingri.texts as txt

router = Router()


@dataclass
class _StubEvent:
    title: str
    starts_at: datetime


async def upcoming_events(days: int = 14) -> list[_StubEvent]:
    """Заглушка вместо сервиса. TODO: заменить запросом в БД."""
    now = datetime.now()
    return [
        _StubEvent("Собрание профкома", now + timedelta(days=2, hours=3)),
        _StubEvent("Сдача отчётов по взносам", now + timedelta(days=9)),
    ]


@router.message(F.text == txt.BTN_EVENTS)
async def events(message: Message) -> None:
    items = await upcoming_events(days=14)
    if not items:
        await message.answer("На ближайшие 2 недели мероприятий нет.")
        return

    text = "\n\n".join(
        f"<b>{e.title}</b>\n{e.starts_at:%d.%m в %H:%M}" for e in items
    )
    await message.answer(f"Ближайшие мероприятия:\n\n{text}")
