import datetime as dt
from enum import StrEnum

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
    Table,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pingri.db.base import Base
from pingri.role import Role


class UserStatus(StrEnum):
    PENDING = "pending"          # заведён админом, ещё не нажал /start
    ACTIVE = "active"
    DEACTIVATED = "deactivated"  # ушёл из профкома; запись не удаляем — на ней висит история


# Многие-ко-многим: человек может быть и в «Председателях», и в «Инфокоме».
user_groups = Table(
    "user_groups",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("group_id", ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    # NULL, пока человек не активировал бота. UNIQUE в Postgres допускает
    # сколько угодно NULL, поэтому неактивированные записи не конфликтуют.
    tg_id: Mapped[int | None] = mapped_column(BigInteger, unique=True, index=True)

    full_name: Mapped[str] = mapped_column(String(200))
    # values_callable обязателен: без него SQLAlchemy кладёт в Postgres ИМЕНА
    # членов энума ('ACTIVE'), а не значения ('active'), и CHECK'и ломаются.
    role: Mapped[Role] = mapped_column(
        Enum(Role, name="user_role", values_callable=lambda e: [m.value for m in e]),
        default=Role.MEMBER,
    )
    status: Mapped[UserStatus] = mapped_column(
        Enum(
            UserStatus,
            name="user_status",
            values_callable=lambda e: [m.value for m in e],
        ),
        default=UserStatus.PENDING,
    )

    # Телеграм может забанить отправку, если человек заблокировал бота.
    can_receive: Mapped[bool] = mapped_column(Boolean, default=True)

    timezone: Mapped[str] = mapped_column(String(64), default="Europe/Moscow")
    # Для справочника: «афиши», «охрана труда», «взносы».
    responsibility: Mapped[str | None] = mapped_column(String(200))
    # Только для отображения ссылки. Идентификатор — всегда tg_id.
    tg_username: Mapped[str | None] = mapped_column(String(64))

    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    activated_at: Mapped[dt.datetime | None] = mapped_column(DateTime(timezone=True))

    groups: Mapped[list["Group"]] = relationship(
        secondary=user_groups, back_populates="members", lazy="selectin"
    )

    __table_args__ = (
        # Активным можно быть только с привязанным tg_id.
        CheckConstraint(
            "status <> 'active' OR tg_id IS NOT NULL", name="active_requires_tg_id"
        ),
    )

    def __repr__(self) -> str:
        return f"<User {self.id} {self.full_name!r} {self.role} {self.status}>"


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str | None] = mapped_column(String(300))

    members: Mapped[list[User]] = relationship(
        secondary=user_groups, back_populates="groups"
    )

    def __repr__(self) -> str:
        return f"<Group {self.id} {self.name!r}>"


class Invite(Base):
    """Одноразовая ссылка t.me/bot?start=<token>, привязанная к заранее
    заведённой записи пользователя."""

    __tablename__ = "invites"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String(64), unique=True, index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))

    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    expires_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True))
    used_at: Mapped[dt.datetime | None] = mapped_column(DateTime(timezone=True))

    user: Mapped[User] = relationship(foreign_keys=[user_id])

    __table_args__ = (
        CheckConstraint("expires_at > created_at", name="invite_expires_after_create"),
    )

    def __repr__(self) -> str:
        return f"<Invite {self.token[:8]}... user={self.user_id} used={self.used_at}>"
