from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


# Люди для справочника и примеров ролей/групп.
MOCK_PEOPLE = [
    {
        "id": 1,
        "name": "Иванов Иван Иванович",
        "role": "chief",
        "groups": ["Председатели", "Профком"],
        "responsibility": "Председатель профкома",
        "telegram": None,
    },
    {
        "id": 2,
        "name": "Петров Пётр Петрович",
        "role": "chief",
        "groups": ["Профком"],
        "responsibility": "Заместитель председателя",
        "telegram": None,
    },
    {
        "id": 3,
        "name": "Сидоров Сидор Сидорович",
        "role": "member",
        "groups": ["Инфоком"],
        "responsibility": "Секретарь",
        "telegram": None,
    },
    {
        "id": 4,
        "name": "Кузнецова Анна Сергеевна",
        "role": "member",
        "groups": ["Профком"],
        "responsibility": "Бухгалтер",
        "telegram": None,
    },
    {
        "id": 5,
        "name": "Смирнова Ольга Викторовна",
        "role": "member",
        "groups": ["Профком"],
        "responsibility": "Юрист",
        "telegram": None,
    },
    {
        "id": 6,
        "name": "Фёдоров Алексей Николаевич",
        "role": "member",
        "groups": ["Профком"],
        "responsibility": "Охрана труда",
        "telegram": None,
    },
    {
        "id": 7,
        "name": "Васильева Мария Александровна",
        "role": "member",
        "groups": ["Профком"],
        "responsibility": "Кадры",
        "telegram": None,
    },
    {
        "id": 8,
        "name": "Козлов Дмитрий Владимирович",
        "role": "member",
        "groups": ["Инфоком"],
        "responsibility": "Информационные технологии",
        "telegram": None,
    },
    {
        "id": 9,
        "name": "Новикова Елена Сергеевна",
        "role": "member",
        "groups": ["Профком"],
        "responsibility": "Социальные вопросы",
        "telegram": None,
    },
    {
        "id": 10,
        "name": "Орлова Наталья Викторовна",
        "role": "member",
        "groups": ["Профком"],
        "responsibility": "Культурно-массовая работа",
        "telegram": None,
    },
]


# Мероприятия и поручения для списка ближайших событий и таблицы главных.
def mock_events(now: datetime | None = None) -> list[dict]:
    now = now or datetime.now(ZoneInfo("Europe/Moscow"))
    return [
        {
            "id": 1,
            "title": "Собрание профкома",
            "event_type": "Рабочая встреча",
            "description": "Обсудить план мероприятий",
            "starts_at": now + timedelta(days=2, hours=3),
            "responsible": ["Иванов Иван Иванович"],
            "group": "Председатели",
            "work_items": [
                {
                    "id": 1,
                    "work_type": "Афиша",
                    "deadline": now + timedelta(days=1),
                    "responsible": "Смирнова Ольга Викторовна",
                },
                {
                    "id": 2,
                    "work_type": "Пост",
                    "deadline": now + timedelta(days=1, hours=6),
                    "responsible": "Сидоров Сидор Сидорович",
                },
            ],
        },
        {
            "id": 2,
            "title": "Сдача отчётов по взносам",
            "event_type": "Отчёт",
            "description": "Собрать отчёты по группам",
            "starts_at": now + timedelta(days=9),
            "responsible": ["Кузнецова Анна Сергеевна"],
            "group": "Профком",
            "work_items": [
                {
                    "id": 3,
                    "work_type": "Текст",
                    "deadline": now + timedelta(days=7),
                    "responsible": "Кузнецова Анна Сергеевна",
                }
            ],
        },
    ]


# Задачи для проверки списка задач и смены статусов.
def mock_tasks(now: datetime | None = None) -> list[dict]:
    now = now or datetime.now(ZoneInfo("Europe/Moscow"))
    return [
        {
            "id": 1,
            "title": "Подготовить афишу",
            "description": "Сделать афишу для собрания профкома",
            "assignee": "Смирнова Ольга Викторовна",
            "deadline": now + timedelta(days=1),
            "link": None,
            "status": "new",
            "comment": None,
        },
        {
            "id": 2,
            "title": "Собрать отчёты по группам",
            "description": "Напомнить председателям и свести ответы",
            "assignee": "Кузнецова Анна Сергеевна",
            "deadline": now + timedelta(days=7),
            "link": None,
            "status": "accepted",
            "comment": None,
        },
    ]
