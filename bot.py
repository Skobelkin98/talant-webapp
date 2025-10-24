import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8219879166:AAHpbP7T35gTV1Ry1F9T37c69mzbt_RehDw"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Ссылка на наше веб-приложение
WEB_APP_URL = "https://talant-webapp-production.up.railway.app"

@dp.message(F.text == "/start")
async def start(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Открыть систему талантов", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])
    await message.answer("Привет! 👋\nНажми, чтобы открыть систему талантов:", reply_markup=kb)


async def main():
    print("Бот запущен...")
    await bot.set_webhook(url="https://talant-webapp-production.up.railway.app/webhook")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
