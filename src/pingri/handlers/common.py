from pingri.config import settings, dp
from aiogram.types import Message, ReplyKeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart, CommandHelp
from pingri import Role

MYTASK = ReplyKeyboardButton(text="Мои задачи")
EVENTS = ReplyKeyboardButton(text="Мероприятия")
DIRECTORY = ReplyKeyboardButton(text="Справочник")
STATUS = ReplyKeyboardButton(text="Статус")
CREATE = ReplyKeyboardButton(text="Создать")


def get_user_role(role: Role) -> ReplyKeyboardMarkup:
     rows = [
        [MYTASK, EVENTS],
        [DIRECTORY],

    ]
    if role in [Role.CHIEF, Role.ADMIN]:
        rows.append([STATUS],[CREATE])
    

    return ReplyKeyboardMarkup(
        keyboard=rows,
        resize_keyboard=True,
         is_persistent=True,
    )



@dp.message(CommandStart())
async def start(message: Message)-> None:
    await message.answer("Привет! Я <b>Pingri</b>. НУ и хз там текст в фото должен быть",reply_markup=get_user_role(Role.MEMBER))
    

@dp.message(CommandHelp())
async def help(message: Message) -> None:
    await message.answer(
        "Я бот для проверки доступности сайтов и сервисов.\n\n"
        "Используйте команду /ping <сайт> для проверки доступности сайта.\n"
        "Например: /ping google.com\n\n"
        "Вы также можете использовать команду /help для получения справки."
    )