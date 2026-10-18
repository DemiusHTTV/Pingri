import pingri.texts as txt

from aiogram import F, Router
from aiogram.types import Message

router = Router() 

@router.message(F.text == txt.BTN_MYTASK)
async def mytask(message: Message) -> None: 
    await message.answer(
        "На данный момент у вас нет задач."
    ) 

