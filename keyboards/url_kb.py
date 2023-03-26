from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_url_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Перейти на сайт", url="https://github.com")
    )
    return builder
