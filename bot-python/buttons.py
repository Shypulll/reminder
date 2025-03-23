from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    """Создает главное меню с кнопками"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 Показать расписание",
                              callback_data="show_schedule")],
        [InlineKeyboardButton(
            text="🔑 Настроить логин и пароль", callback_data="setup_login")],
        [InlineKeyboardButton(text="ℹ️ О боте", callback_data="about_bot")]
    ])
    return keyboard
