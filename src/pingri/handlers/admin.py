import pingrt.text as text
from aiogram import F, Router
from aiogram.types import Message

router = Router()


@router.message(F.text == text.BTN_CREATE)
async def create(message: Message) -> None:
    await message.answer(
        "Функция создания задач пока недоступна."
    )

@router.message(F.text == text.BTN_STATUS)
async def status(message: Message) -> None:
    await message.answer(
        "Функция проверки статуса задач пока недоступна."
    )
    
