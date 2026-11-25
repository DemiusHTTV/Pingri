import datetime as dt

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pingri.db.models import Group, Invite, User, UserStatus
from pingri.role import Role


class UserRepository:
    """Единственное место в проекте, где живут запросы к users.

    Снаружи зовут методы по именам — никто не знает и не должен знать,
    собран запрос через select() или написан сырым SQL.
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # --- чтение -------------------------------------------------------

    async def get_by_tg_id(self, tg_id: int) -> User | None:
        return await self.session.scalar(select(User).where(User.tg_id == tg_id))

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def list_by_role(self, role: Role) -> list[User]:
        rows = await self.session.scalars(
            select(User)
            .where(User.role == role, User.status == UserStatus.ACTIVE)
            .order_by(User.full_name)
        )
        return list(rows)

    async def list_not_activated(self) -> list[User]:
        """Кого завели, но бот им писать не может. Главному это нужно видеть,
        иначе он назначит мероприятие на того, до кого напоминание не дойдёт."""
        rows = await self.session.scalars(
            select(User)
            .where(User.status == UserStatus.PENDING)
            .order_by(User.full_name)
        )
        return list(rows)

    async def group_members(self, group_name: str) -> list[User]:
        """Активные получатели группы — для рассылок и назначения мероприятий."""
        rows = await self.session.scalars(
            select(User)
            .join(User.groups)
            .where(
                Group.name == group_name,
                User.status == UserStatus.ACTIVE,
                User.can_receive.is_(True),
            )
            .order_by(User.full_name)
        )
        return list(rows)

    # --- запись -------------------------------------------------------

    async def create_pending(
        self,
        full_name: str,
        role: Role = Role.MEMBER,
        responsibility: str | None = None,
        groups: list[Group] | None = None,
    ) -> User:
        """Завести человека ДО того, как он нажал /start. tg_id ещё неизвестен.

        Группы принимаем сразу: присвоить коллекцию можно только пока объект
        не ушёл в базу. После flush обращение к user.groups потребует
        подгрузки, а ленивая загрузка в async падает с MissingGreenlet.
        """
        user = User(full_name=full_name, role=role, responsibility=responsibility)
        if groups:
            user.groups = list(groups)
        self.session.add(user)
        await self.session.flush()   # INSERT ... RETURNING id, но без COMMIT
        return user

    async def add_to_group(self, user: User, group: Group) -> None:
        """Для уже сохранённого пользователя коллекцию надо сперва подтянуть
        явно — сама она в async не догрузится."""
        await self.session.refresh(user, attribute_names=["groups"])
        if group not in user.groups:
            user.groups.append(group)
            await self.session.flush()

    async def activate(self, user: User, tg_id: int, username: str | None) -> User:
        """Привязать телеграм-аккаунт к заранее заведённой записи."""
        user.tg_id = tg_id
        user.tg_username = username
        user.status = UserStatus.ACTIVE
        user.activated_at = dt.datetime.now(dt.UTC)
        await self.session.flush()
        return user

    async def mark_unreachable(self, user: User) -> None:
        """Юзер заблокировал бота — снимаем флаг, чтобы не долбиться впустую."""
        user.can_receive = False
        await self.session.flush()

    # --- инвайты ------------------------------------------------------

    async def get_valid_invite(self, token: str) -> Invite | None:
        """Одноразовый и непросроченный. Проверка в SQL, а не в Python:
        так гонка между двумя нажатиями не создаст двух активаций."""
        return await self.session.scalar(
            select(Invite).where(
                Invite.token == token,
                Invite.used_at.is_(None),
                Invite.expires_at > dt.datetime.now(dt.UTC),
            )
        )
