import sqlite3
import json
import os

# Проверяем наличие data.json
if os.path.exists("data.json"):
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = {}  # Если файла нет, начинаем с пустого словаря

# Подключаемся к базе данных SQLite
conn = sqlite3.connect("talents.db")
c = conn.cursor()

# Создаём таблицу, если она ещё не существует
c.execute('''CREATE TABLE IF NOT EXISTS talents (name TEXT PRIMARY KEY, points INTEGER)''')

# Импортируем данные из data.json в таблицу
c.executemany("INSERT OR REPLACE INTO talents (name, points) VALUES (?, ?)", list(data.items()))

# Сохраняем изменения
conn.commit()

# Закрываем соединение
conn.close()

print("Данные импортированы в talents.db")
