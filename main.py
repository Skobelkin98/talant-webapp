from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json, os

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

# ---------- Веб-интерфейс ----------
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ---------- API ----------
def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                data = {}
            return data
    except Exception:
        return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.get("/api/data", response_class=JSONResponse)
def get_data():
    return load_data()

@app.post("/api/add", response_class=JSONResponse)
async def add_user(request: Request):
    payload = await request.json()
    name = payload.get("name", "").strip()
    points = int(payload.get("points", 0))
    data = load_data()
    if name:
        data[name] = data.get(name, 0) + points
        save_data(data)
    return {"status": "ok", "data": data}

@app.post("/api/delete", response_class=JSONResponse)
async def delete_user(request: Request):
    payload = await request.json()
    name = payload.get("name", "").strip()
    data = load_data()
    if name in data:
        del data[name]
        save_data(data)
    return {"status": "ok", "data": data}

# ---------- Webhook от Telegram ----------
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print("Webhook received:", data)  # Для отладки в логах
    return JSONResponse(status_code=200, content={})
