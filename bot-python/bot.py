import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 🔐 Телеграм-токен и ID чата
TOKEN = "7156477479:AAEOJE5ge2QcgzOko9TazY96bsz_p1xy6uY"
CHAT_ID = 1057220053

# 🔧 Настройка бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 🔄 Глобальные переменные
sent_notifications = set()
current_schedule = []
user_credentials = {}  # Храним логины и пароли пользователей

# 🔧 Путь к ChromeDriver
CHROMEDRIVER_PATH = "C:/Users/User/Downloads/chromedriver.exe"

# 🌐 URL дневника
DIARY_URL = "https://mojeaeh.vizja.pl/vizja-stud-app/ledge/view/ImapLogin"

# 📌 Создание кнопок меню


def main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 Показать расписание",
                              callback_data="show_schedule")],
        [InlineKeyboardButton(
            text="🔑 Настроить логин и пароль", callback_data="setup_login")],
        [InlineKeyboardButton(text="ℹ️ О боте", callback_data="about_bot")],
        # Новая кнопка
        [InlineKeyboardButton(
            text="📜 Функции", callback_data="functions_list")]
    ])
    return keyboard

# 📌 Основное меню


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("✅ Бот запущен! Выберите действие:", reply_markup=main_menu())

# 📌 Обработчик кнопок


@dp.callback_query(lambda callback: callback.data in ["show_schedule", "setup_login", "about_bot", "functions_list"])
async def callback_handler(callback: CallbackQuery):
    if callback.data == "show_schedule":
        await show_schedule(callback)
        # Показываем меню снова
        await callback.message.answer("🏠 Главное меню:", reply_markup=main_menu())
    elif callback.data == "setup_login":
        await setup_login(callback)
        # Показываем меню снова
        await callback.message.answer("🏠 Главное меню:", reply_markup=main_menu())
    elif callback.data == "about_bot":
        await about_bot(callback)
        # Показываем меню снова
        await callback.message.answer("🏠 Главное меню:", reply_markup=main_menu())
    elif callback.data == "functions_list":
        # Главное меню не показываем, чтобы не мешало
        await functions_list(callback)

# 📌 Отображение расписания


async def show_schedule(callback: CallbackQuery):
    global current_schedule
    if not current_schedule:
        await callback.message.answer("📌 Ваше расписание пока не загружено. Используйте /login для входа.")
        return
    text = "📅 *Ваше расписание на сегодня:*\n"
    for lesson in current_schedule:
        text += (
            f"\n📌 {lesson['subject']}"
            f"\n🕒 {lesson['start_time']} - {lesson['end_time']}"
            f"\n👨‍🏫 {lesson['teacher']}"
            f"\n🏢 {lesson['location']}\n"
        )
    await callback.message.answer(text, parse_mode=ParseMode.MARKDOWN)

# 📌 Настройка логина


async def setup_login(callback: CallbackQuery):
    await callback.message.answer("🔑 Введите ваш логин:")
    user_credentials[CHAT_ID] = [None, None]

# 📌 Описание бота


async def about_bot(callback: CallbackQuery):
    text = (
        "ℹ️ *Этот бот помогает отслеживать расписание занятий!*\n\n"
        "✅ Получает расписание из студенческого портала.\n"
        "✅ Отправляет уведомления о начале и окончании занятий."
    )
    await callback.message.answer(text, parse_mode=ParseMode.MARKDOWN)

# 📌 Функции бота (новая команда)


async def functions_list(callback: CallbackQuery):
    text = (
        "📜 *Список команд и функций:*\n\n"
        "✅ /start – Запустить бота и открыть главное меню.\n"
        "✅ /schedule – Показать расписание на текущую или следующую неделю.\n"
        "✅ /login – Ввести логин и пароль для получения расписания.\n"
        "✅ /help – Показать помощь и описание команд.\n"
        "✅ /about – Описание работы бота.\n\n"
        "⚙️ Также доступны кнопки в меню для управления расписанием!"
    )
    await callback.message.answer(text, parse_mode=ParseMode.MARKDOWN)

# 📌 ОБРАБОТЧИК ЛЮБЫХ ДРУГИХ СООБЩЕНИЙ (не команд и не кнопок)


@dp.message()
async def handle_unknown_message(message: Message):
    await message.answer("🏠 Главное меню:", reply_markup=main_menu())

# 📌 Главная функция


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
