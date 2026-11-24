import pingri.texts as txt

from aiogram import F, Router
from aiogram.types import Message

from pingri.mock_data import MOCK_PEOPLE

router = Router()


@router.message(F.text == txt.BTN_DIRECTORY)
async def directory(message: Message) -> None:
    rows = [
        f"{index}. {person['name']} — {person['responsibility']}"
        for index, person in enumerate(MOCK_PEOPLE, start=1)
    ]
    await message.answer("Справочник профкома:\n\n" + "\n".join(rows))
