import sqlite3
from datetime import datetime
from schedule_data import get_weekly_schedule  # Берём данные из отдельного файла

NAMEDB = "skibididatabase.db"

# создается таблица
def init_db():
    conn = sqlite3.connect(NAMEDB)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            username TEXT,
            first_request_date TEXT,
            last_request_date TEXT,
            total_requests INTEGER DEFAULT 1
        )
    ''')
    conn.commit()
    conn.close()

# Сохранить нового пользователя
def save_user(user_id, username):
    conn = sqlite3.connect(NAMEDB)
    cursor = conn.cursor()
    
    # проверка
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    exists = cursor.fetchone()
    
    if not exists:
        now = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO users (user_id, username, first_request_date, last_request_date, total_requests)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, now, now, 1))
        conn.commit()
    conn.close()

# Обновить время последнего запроса расписания
def update_user_last_request(user_id):
    conn = sqlite3.connect(NAMEDB)
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    
    cursor.execute('''
        UPDATE users 
        SET last_request_date = ?, total_requests = total_requests + 1
        WHERE user_id = ?
    ''', (now, user_id))
    conn.commit()
    conn.close()

# расписание
def get_full_schedule():
    schedule = get_weekly_schedule()
    
    if not schedule:
        return "📅 Расписание временно недоступно. Попробуй позже."
    
    result = "📚 <b>Расписание уроков супер онлайн-школы</b>\n\n"
    for day, lessons in schedule.items():
        result += f"<b>{day}</b>\n"
        if lessons:
            for lesson in lessons:
                result += f"  • {lesson['time']} - {lesson['name']} ({lesson['teacher']})\n"
        else:
            result += "  • Нет уроков\n"
        result += "\n"
    
    return result