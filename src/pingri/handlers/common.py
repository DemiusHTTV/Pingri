from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from pingri.role import Role

router = Router()

MYTASK = KeyboardButton(text="Мои задачи")
EVENTS = KeyboardButton(text="Мероприятия")
DIRECTORY = KeyboardButton(text="Справочник")
STATUS = KeyboardButton(text="Статус")
CREATE = KeyboardButton(text="Создать")


def main_menu(role: Role) -> ReplyKeyboardMarkup:
    rows = [
        [MYTASK, EVENTS],
        [DIRECTORY],
    ]
    if role in (Role.CHIEF, Role.ADMIN):
        rows.append([STATUS, CREATE])

    return ReplyKeyboardMarkup(
        keyboard=rows,
        resize_keyboard=True,
        is_persistent=True,
    )


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        "Привет! Я <b>Pingri</b>.",
        reply_markup=main_menu(Role.MEMBER),
    )


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(
        "Я напоминаю о мероприятиях и задачах профкома.\n\n"
        "Кнопки внизу экрана — основное меню."
    )
