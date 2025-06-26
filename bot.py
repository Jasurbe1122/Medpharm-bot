from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import ChatMemberAdministrator, ChatMemberOwner
from dotenv import load_dotenv
import os, sqlite3
from ai_parser import parse_text
from pdf_utils import generate_pdf_report
from utils import save_expense

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or "YOUR_BOT_TOKEN"

def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (user_id TEXT, chat_id TEXT, date TEXT, category TEXT, amount REAL, person TEXT, place TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS users (user_id TEXT, first_name TEXT)''')
    conn.commit()
    conn.close()

async def handle_message(update, context):
    user_id = str(update.message.from_user.id)
    chat_id = str(update.message.chat_id)
    text = update.message.text
    parsed_data = parse_text(text)
    if parsed_data:
        save_expense(user_id, chat_id, parsed_data)
        await update.message.reply_text(f"✅ {parsed_data['category']} uchun {parsed_data['amount']} so‘m saqlandi. Yana nima?")
    else:
        await update.message.reply_text("Matnni tushunolmadim. Aniqlik kiriting.")

async def group_report(update, context):
    chat_id = str(update.message.chat_id)
    user = await context.bot.get_chat_member(chat_id, update.message.from_user.id)
    if not isinstance(user, (ChatMemberAdministrator, ChatMemberOwner)):
        await update.message.reply_text("Faqat adminlar hisobotni ko‘ra oladi!")
        return
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT u.first_name, e.category, e.amount, e.place, e.date FROM expenses e JOIN users u ON e.user_id = u.user_id WHERE e.chat_id = ?", (chat_id,))
    expenses = c.fetchall()
    conn.close()
    if not expenses:
        await update.message.reply_text("Guruhda xarajat yo‘q.")
        return
    pdf_file = generate_pdf_report(expenses, chat_id)
    await context.bot.send_document(chat_id=chat_id, document=open(pdf_file, 'rb'), filename="guruh_hisobot.pdf")

def main():
    init_db()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("guruhhisobot", group_report))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
