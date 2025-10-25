from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json, os
from aiogram import Bot, Dispatcher
from aiogram.types import Update
import asyncio

# Токен и авторизованные юзернеймы
TOKEN = "8219879166:AAHpbP7T35gTV1Ry1F9T37c69mzbt_RehDw"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Список разрешённых юзернеймов (добавьте нужные, например, свои)
ALLOWED_EDITORS = {"Pavel_Skobyolkin", "dariaskob", "Wolfram183", "artem_Christian"}  # Добавьте другие юзернеймы сюда

app = FastAPI()

# Пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")

# Гарантируем наличие data.json
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=2)

# Подключаем фронтенд
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Хэндлер для /start
@dp.message(lambda message: message.text == "/start")
async def start_handler(update: Update, context=None):
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Открыть систему талантов", web_app=WebAppInfo(url="https://talant-webapp-production.up.railway.app"))]
    ])
    await bot.send_message(update.message.chat.id, "Привет! 👋\nНажми, чтобы открыть систему талантов:", reply_markup=kb)

# Загрузка данных
def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                data = {}
            return data
    except Exception:
        return {}

# Сохранение данных
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Веб-интерфейс
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API
@app.get("/api/data", response_class=JSONResponse)
def get_data():
    return load_data()

@app.post("/api/add", response_class=JSONResponse)
async def add_user(request: Request):
    payload = await request.json()
    name = payload.get("name", "").strip()
    points = int(payload.get("points", 0))
    username = request.headers.get("X-Telegram-Username", "").strip()
    data = load_data()
    if not username:
        return {"status": "error", "message": "No username provided"}
    if username in ALLOWED_EDITORS and name:
        data[name] = data.get(name, 0) + points
        save_data(data)
    return {"status": "ok", "data": data}

@app.post("/api/delete", response_class=JSONResponse)
async def delete_user(request: Request):
    payload = await request.json()
    name = payload.get("name", "").strip()
    username = request.headers.get("X-Telegram-Username", "").strip()
    data = load_data()
    if not username:
        return {"status": "error", "message": "No username provided"}
    if username in ALLOWED_EDITORS and name in data:
        del data[name]
        save_data(data)
    return {"status": "ok", "data": data}

# Webhook
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update(**data)
    await dp.feed_update(bot, update)
    return JSONResponse(status_code=200, content={})



