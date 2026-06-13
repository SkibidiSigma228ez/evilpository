import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.session.aiohttp import AiohttpSession  # <-- 1. Импортируем сессию
from config import BOT_TOKEN
from logic import init_db, get_full_schedule, save_user, update_user_last_request


# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Клавиатура с кнопкой
def get_main_keyboard():
    button = KeyboardButton(text="📚 Получить расписание")
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True  # чтобы кнопка была красивой
    )
    return keyboard

#/start (асинк это чтобы несколько людей могли обрабатывать запрос и код не стопорился бы на одном)
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"
    save_user(user_id, username)
    
    welcome_text = (
        "👋 Добро пожаловать в бот расписания онлайн-школы!\n\n"
        "Нажми на кнопку ниже, чтобы получить расписание всех уроков."
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard())

#кнопка расписания 
@dp.message(lambda message: message.text == "📚 Получить расписание")
async def send_schedule(message: types.Message):
    user_id = message.from_user.id
    update_user_last_request(user_id)  # запрос логируется в датабазу
    
    schedule_text = get_full_schedule()
    await message.answer(schedule_text, parse_mode="HTML")

# запускк
async def main():
    init_db()  
    print("✅ Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())