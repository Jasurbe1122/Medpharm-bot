from telegram.ext import Application
from datetime import datetime

async def send_reminder(context):
    job = context.job
    await context.bot.send_message(chat_id=job.context, text="Xarajatlaringizni yozdingizmi?")

def check_balance(user_id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ?", (user_id,))
    total = c.fetchone()[0] or 0
    conn.close()
    return total
