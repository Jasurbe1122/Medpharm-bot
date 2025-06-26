from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import ChatMemberAdministrator, ChatMemberOwner
from dotenv import load_dotenv
import os
import sqlite3
from datetime import datetime
import logging  # Xatolarni aniqlash uchun logging qo‘shildi

# utils.py, ai_parser, pdf_utils modullarini import qilish
try:
    from utils import save_expense
    from ai_parser import parse_text
    from pdf_utils import generate_pdf_report
except ImportError as e:
    print(f"Modul topilmadi: {e}")
    raise

# Logging sozlamalari
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Tokenni yuklash
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN .env faylida topilmadi!")

# Ma'lumotlar bazasini yaratish
def init_db():
    try:
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS expenses
                     (user_id TEXT, chat_id TEXT, date TEXT, category TEXT, amount REAL, person TEXT, place TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (user_id TEXT, first_name TEXT)''')
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Ma'lumotlar bazasi xatosi: {e}")
    finally:
        conn.close()

# Foydalanuvchi ma'lumotlarini saqlash
def save_user(user_id, first_name):
    try:
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO users (user_id, first_name) VALUES (?, ?)", (user_id, first_name))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Foydalanuvchi saqlashda xato: {e}")
    finally:
        conn.close()

# Matnni qabul qilish
async def handle_message(update, context):
    try:
        user_id = str(update.message.from_user.id)
        first_name = update.message.from_user.first_name
        chat_id = str(update.message.chat_id)
        text = update.message.text

        # Foydalanuvchini saqlash
        save_user(user_id, first_name)

        parsed_data = parse_text(text)
        if parsed_data:
            save_expense(user_id, chat_id, parsed_data)
            await update.message.reply_text(f"✅ {parsed_data['category']} uchun {parsed_data['amount']} so‘m saqlandi. Yana nima?")
        else:
            await update.message.reply_text("Matnni tushunolmadim. Iltimos, aniqroq yozing.")
    except Exception as e:
        logger.error(f"Xabar ishlov berishda xato: {e}")
        await update.message.reply_text("Xato yuz berdi, qayta urinib ko‘ring.")

# Guruh uchun hisobot
async def group_report(update, context):
    try:
        chat_id = str(update.message.chat_id)
        user = await context.bot.get_chat_member(chat_id, update.message.from_user.id)

        if not isinstance(user, (ChatMemberAdministrator, ChatMemberOwner)):
            await update.message.reply_text("Faqat adminlar hisobotni ko‘ra oladi!")
            return

        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute('''SELECT u.first_name, e.category, e.amount, e.place, e.date
                     FROM expenses e JOIN users u ON e.user_id = u.user_id
                     WHERE e.chat_id = ?''', (chat_id,))
        expenses = c.fetchall()
        conn.close()

        if not expenses:
            await update.message.reply_text("Guruhda xarajat yo‘q.")
            return

        pdf_file = generate_pdf_report(expenses, chat_id)
        await context.bot.send_document(chat_id=chat_id, document=open(pdf_file, 'rb'), filename="guruh_hisobot.pdf")
    except Exception as e:
        logger.error(f"Hisobot yaratishda xato: {e}")
        await update.message.reply_text("Hisobot yaratishda xato yuz berdi.")

# Asosiy ishga tushirish funksiyasi
async def main():
    init_db()
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("guruhhisobot", group_report))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot ishga tushdi...")
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
