from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Общий предок всех моделей. Alembic берёт схему из Base.metadata."""
