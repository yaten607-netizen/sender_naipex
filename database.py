import sqlite3
import os

# Путь к базе данных на флешке Railway. 
# Если запускаешь на компе локально, он создаст папку data прямо в проекте.
DB_DIR = "/app/data" if os.path.exists("/app") else "data"
DB_PATH = os.path.join(DB_DIR, "bot_data.db")

def init_db():
    # Создаем папку, если её нет
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Таблица пользователей бота
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            language TEXT DEFAULT 'rus'
        )
    """)
    
    # 2. Таблица текстов сообщений для рассылки
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            user_id INTEGER PRIMARY KEY,
            text_content TEXT DEFAULT ''
        )
    """)
    
    # 3. Таблица групп/чатов для рассылки
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS target_groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            group_url TEXT,
            status INTEGER DEFAULT 1
        )
    """)
    
    conn.commit()
    conn.close()
    print("[+] База данных и таблицы успешно инициализированы!")