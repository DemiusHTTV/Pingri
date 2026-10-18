import pingri.texts as txt
from aiogram import F, Router
from aiogram.types import Message

router = Router()


@router.message(F.text == txt.BTN_CREATE)
async def create(message: Message) -> None:
    await message.answer(
        "Функция создания задач пока недоступна."
    )

@router.message(F.text == txt.BTN_STATUS)
async def status(message: Message) -> None:
    await message.answer(
        "Функция проверки статуса задач пока недоступна."
    )
    
