import sqlite3
from datetime import datetime

def save_expense(user_id, chat_id, data):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("INSERT INTO expenses VALUES (?, ?, ?, ?, ?, ?, ?)",
              (user_id, chat_id, datetime.now().strftime('%Y-%m-%d'), data['category'], data['amount'], data['person'], data['place']))
    c.execute("INSERT OR IGNORE INTO users VALUES (?, ?)", (user_id, data['person'] or 'Foydalanuvchi'))
    conn.commit()
    conn.close()