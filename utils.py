
import sqlite3

def save_expense(user_id, data):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS expenses (user_id TEXT, name TEXT, amount INTEGER, unit TEXT)")
    c.execute("INSERT INTO expenses VALUES (?, ?, ?, ?)", (user_id, data['name'], data['amount'], data['unit']))
    conn.commit()
    conn.close()

def get_summary_text(user_id):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT name, SUM(amount) FROM expenses WHERE user_id = ? GROUP BY name", (user_id,))
    summary = c.fetchall()
    conn.close()
    return "\n".join([f"{name}: {amount}" for name, amount in summary])
