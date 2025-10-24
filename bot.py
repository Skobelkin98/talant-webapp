import asyncio
from aiogram import Bot

TOKEN = "8219879166:AAHpbP7T35gTV1Ry1F9T37c69mzbt_RehDw"
bot = Bot(token=TOKEN)

WEB_APP_URL = "https://talant-webapp-production.up.railway.app"

async def main():
    print("Установка webhook...")
    await bot.set_webhook(url="https://talant-webapp-production.up.railway.app/webhook")
    print("Webhook успешно установлен. Бот завершил работу.")

if __name__ == "__main__":
    asyncio.run(main())
