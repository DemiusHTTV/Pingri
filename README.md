# Pingri

Pingri — backend для мероприятий, задач и справочника команды. Сейчас данные лежат в памяти процесса: после перезапуска они пропадут. PostgreSQL в этой версии не используется API.

## Папки

- `src/pingri/api/` — HTTP-ручки, модели запросов и временное хранилище.
- `src/pingri/handlers/` — обработчики Telegram-бота.
- `src/pingri/db/` — модели и запросы к PostgreSQL; API пока их не вызывает.
- `src/pingri/mock_data.py` — общие примеры данных для людей, мероприятий, поручений и задач.

В `mock_data.py`:

- `MOCK_PEOPLE` — записи справочника и группы.
- `mock_events()` — мероприятия и поручения с дедлайнами.
- `mock_tasks()` — примеры задач и их статусов.

Моки автоматически загружаются в API только когда задано `LOAD_MOCK_DATA=true`.

## Локальный запуск API

Нужны Python 3.13 и `uv`.

```bash
uv sync
```

Создай локальный файл `.dev.vars`:

```env
API_KEY=local-dev-key
CHIEF_API_KEY=chief-view-key
LOAD_MOCK_DATA=true
```

Запусти локальный Cloudflare Worker:

```bash
uv run pywrangler dev
```

Проверка доступности: `GET http://localhost:8787/health`. Для обычных ручек передавай `X-API-Key: local-dev-key`, для обзора главных — `X-Chief-Key: chief-view-key`.

## Ручки

| Метод | Путь | Что делает |
| --- | --- | --- |
| `GET` | `/health` | Проверяет, что API запущен |
| `GET` | `/api/people?search=афиши` | Ищет людей по имени или ответственности |
| `POST` | `/api/people` | Добавляет человека в справочник |
| `DELETE` | `/api/people/{id}` | Удаляет человека |
| `GET` | `/api/events?days=14` | Показывает ближайшие мероприятия |
| `POST` | `/api/events` | Создаёт мероприятие |
| `DELETE` | `/api/events/{id}` | Удаляет мероприятие |
| `GET` | `/api/overview/workload` | Таблица поручений для главных: тип мероприятия, что сделать, срок и ответственный |
| `GET` | `/api/overview/workload.csv` | Скачать эту таблицу как CSV и открыть в Excel или Google Sheets |
| `GET` | `/api/tasks?assignee=Имя` | Показывает задачи, при желании — одного исполнителя |
| `POST` | `/api/tasks` | Ставит задачу |
| `PATCH` | `/api/tasks/{id}` | Меняет статус и комментарий задачи |
| `DELETE` | `/api/tasks/{id}` | Удаляет задачу |

Тела запросов и ответы можно посмотреть в Swagger: `/docs`.

Пример создания мероприятия:

```json
{
  "title": "Собрание",
  "event_type": "Рабочая встреча",
  "description": "Подготовить список вопросов",
  "starts_at": "2026-12-01T18:30:00+03:00",
  "responsible": ["Иван Иванов"],
  "group": "Председатели",
  "work_items": [
    {
      "work_type": "Афиша",
      "deadline": "2026-11-28T18:00:00+03:00",
      "responsible": "Иван Иванов"
    },
    {
      "work_type": "Пост",
      "deadline": "2026-11-29T12:00:00+03:00",
      "responsible": "Анна Петрова"
    }
  ]
}
```

У дат нужен часовой пояс. Для задачи статусы: `new`, `accepted`, `cannot`, `done`. При статусе `cannot` нужно заполнить `comment`.

## Cloudflare

Worker entrypoint находится в `src/worker.py`. Если подключаешь репозиторий через Cloudflare Builds, поставь команды:

- Build command: `uv sync`
- Deploy command: `uv run pywrangler deploy`

Используй `pywrangler deploy`, а не `npx wrangler deploy`: он подготавливает Python-модули для Worker. Entry point лежит прямо в `src/`, чтобы импорты пакета `pingri` находились в сборке. Имя Worker в Cloudflare Builds должно быть `pingri`, как в `wrangler.jsonc`.

Для ручного деплоя из терминала:

```bash
uv run pywrangler deploy
uv run pywrangler secret put API_KEY
uv run pywrangler secret put CHIEF_API_KEY
```

HTTP API можно развернуть на Cloudflare уже сейчас. Telegram polling-бот из `src/pingri/main.py` — отдельный процесс; его webhook-подключение будет следующим шагом. Временное хранилище Worker подходит для разработки, но Cloudflare может запускать несколько копий и перезапускать их. Для общих и постоянных данных позже понадобится D1 или другое хранилище.

Не добавляй `LOAD_MOCK_DATA=true` в настройки production Worker: иначе он покажет примеры из `mock_data.py`.
