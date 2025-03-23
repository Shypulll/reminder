import asyncio
import logging
import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram import F
from datetime import datetime, timedelta

# 🔐 Телеграм-токен и ID чата
TOKEN = "7156477479:AAEOJE5ge2QcgzOko9TazY96bsz_p1xy6uY"
CHAT_ID = 1057220053

# 🔧 Настройка бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

# 🔄 Глобальные переменные
sent_notifications = set()
current_schedule = []
notifications_enabled = True

# 📁 Путь к JSON-файлу для хранения логинов
CREDENTIALS_FILE = "user_data.json"

# 📦 Состояния FSM


class LoginState(StatesGroup):
    waiting_for_login = State()
    waiting_for_password = State()

# 📋 Главное меню


def main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 Показать расписание",
                              callback_data="show_schedule")],
        [InlineKeyboardButton(text="🔔 Включить уведомления",
                              callback_data="enable_notifications")],
        [InlineKeyboardButton(text="🔕 Отключить уведомления",
                              callback_data="disable_notifications")],
        [InlineKeyboardButton(text="🔑 Ввести логин и пароль",
                              callback_data="enter_credentials")],
        [InlineKeyboardButton(text="ℹ️ О боте", callback_data="about_bot")]
    ])
    return keyboard


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("✅ Бот запущен! Выберите действие:", reply_markup=main_menu())


@dp.callback_query(F.data == "show_schedule")
async def show_schedule(callback: CallbackQuery):
    if not current_schedule:
        await callback.message.answer("📌 Ваше расписание пока не загружено. Используйте кнопку 'Ввести логин и пароль'.")
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


@dp.callback_query(F.data == "enable_notifications")
async def enable_notifications(callback: CallbackQuery):
    global notifications_enabled
    notifications_enabled = True
    await callback.message.answer("🔔 Уведомления включены!")


@dp.callback_query(F.data == "disable_notifications")
async def disable_notifications(callback: CallbackQuery):
    global notifications_enabled
    notifications_enabled = False
    await callback.message.answer("🔕 Уведомления отключены!")


@dp.callback_query(F.data == "about_bot")
async def about_bot(callback: CallbackQuery):
    text = (
        "ℹ️ *Этот бот помогает отслеживать расписание занятий!*\n\n"
        "✅ Получает расписание из студенческого портала.\n"
        "✅ Отправляет уведомления о начале и окончании занятий."
    )
    await callback.message.answer(text, parse_mode=ParseMode.MARKDOWN)


@dp.callback_query(F.data == "enter_credentials")
async def process_cred_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("✍️ Введите логин:")
    await state.set_state(LoginState.waiting_for_login)


@dp.message(LoginState.waiting_for_login)
async def get_login(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("🔒 Теперь введите пароль:")
    await state.set_state(LoginState.waiting_for_password)


@dp.message(LoginState.waiting_for_password)
async def get_password(message: Message, state: FSMContext):
    user_data = await state.get_data()
    login = user_data['login']
    password = message.text
    user_id = str(message.from_user.id)

    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    # 🔁 Обновляем структуру JSON с полем id и users
    data["id"] = user_id
    if "users" not in data:
        data["users"] = {}
    data["users"][user_id] = {"username": login, "password": password}

    with open(CREDENTIALS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    await message.answer("✅ Логин и пароль сохранены!")
    await state.clear()


async def send_notifications():
    global notifications_enabled
    while True:
        if notifications_enabled and current_schedule:
            now = datetime.now().strftime('%Y-%m-%d %H:%M')
            for lesson in current_schedule:
                try:
                    if "start_time" not in lesson:
                        logging.warning(
                            "⚠️ Ошибка: У занятия отсутствует start_time.")
                        continue

                    notification_time = (datetime.strptime(
                        lesson["start_time"], '%Y-%m-%d %H:%M') - timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M')
                    if notification_time == now and notification_time not in sent_notifications:
                        text = (
                            f"⏳ *Скоро начнется занятие!*\n\n"
                            f"📌 {lesson['subject']}\n"
                            f"🕒 {lesson['start_time']} - {lesson['end_time']}\n"
                            f"👨‍🏫 {lesson['teacher']}\n"
                            f"🏢 {lesson['location']}"
                        )
                        await bot.send_message(CHAT_ID, text, parse_mode=ParseMode.MARKDOWN)
                        sent_notifications.add(notification_time)
                except Exception as e:
                    logging.error(f"Ошибка отправки уведомления: {e}")
        await asyncio.sleep(60)


async def main():
    logging.basicConfig(level=logging.INFO)
    asyncio.create_task(send_notifications())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
