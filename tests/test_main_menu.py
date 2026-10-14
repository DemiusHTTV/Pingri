import pytest
from aiogram.types import ReplyKeyboardMarkup

from pingri.handlers.common import (
    CREATE,
    DIRECTORY,
    EVENTS,
    MYTASK,
    STATUS,
    main_menu,
)
from pingri.role import Role

PRIVILEGED = [Role.CHIEF, Role.ADMIN]


def labels(markup: ReplyKeyboardMarkup) -> list[str]:
    """Плоский список подписей кнопок — без разбивки по строкам."""
    return [button.text for row in markup.keyboard for button in row]


def test_member_sees_only_base_buttons():
    assert labels(main_menu(Role.MEMBER)) == [
        MYTASK.text,
        EVENTS.text,
        DIRECTORY.text,
    ]


def test_member_cannot_see_privileged_buttons():
    menu = labels(main_menu(Role.MEMBER))
    assert CREATE.text not in menu
    assert STATUS.text not in menu


@pytest.mark.parametrize("role", PRIVILEGED)
def test_privileged_roles_see_create_and_status(role: Role):
    menu = labels(main_menu(role))
    assert CREATE.text in menu
    assert STATUS.text in menu


@pytest.mark.parametrize("role", PRIVILEGED)
def test_privileged_roles_keep_base_buttons(role: Role):
    """Права накапливаются: главный и админ видят всё, что видит участник."""
    menu = labels(main_menu(role))
    for button in (MYTASK, EVENTS, DIRECTORY):
        assert button.text in menu


@pytest.mark.parametrize("role", list(Role))
def test_layout_flags_are_set(role: Role):
    menu = main_menu(role)
    assert menu.resize_keyboard is True
    assert menu.is_persistent is True
    # главное меню не должно сворачиваться после первого нажатия
    assert menu.one_time_keyboard is not True


@pytest.mark.parametrize("role", list(Role))
def test_rows_are_not_shared_between_calls(role: Role):
    """Кнопки лежат в модульных константах — важно, чтобы сборка меню
    не мутировала их и не копила строки между вызовами."""
    first = main_menu(role)
    first.keyboard.append([CREATE])

    assert labels(main_menu(role)) == labels(main_menu(role))
