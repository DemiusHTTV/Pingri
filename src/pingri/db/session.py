from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from pingri.config import settings

# Движок создаётся ОДИН раз на всё приложение: внутри него пул соединений.
# Это не «открыть файл на каждый запрос», как было в sqlite3.
engine: AsyncEngine = create_async_engine(
    settings.postgres_dsn,
    echo=False,     # True — и в лог посыпется весь реальный SQL, удобно для отладки
    pool_size=5,
    max_overflow=5,
    pool_pre_ping=True,   # проверять живость соединения: Postgres рвёт простаивающие
)

# Фабрика сессий. Одна сессия = одна транзакция = один апдейт от Telegram.
session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # иначе после commit доступ к полям полезет в БД заново
)
