
import os
import logging
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, filters
)
from ai_parser import parse_text
from csv_utils import save_to_csv
from pdf_utils import generate_pdf
from scheduler import setup_schedulers
from utils import is_admin, get_username

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

app = Application.builder().token(TOKEN).build()
setup_schedulers(app)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Medpharm xarajat botiga xush kelibsiz!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    username = get_username(user)
    text = update.message.text

    parsed = parse_text(text)
    if parsed:
        save_to_csv(user.id, username, parsed)
        await update.message.reply_text(
            f"✅ {parsed['name']} uchun {parsed['amount']}, {parsed['price']} so'm saqlandi."
        )
    else:
        await update.message.reply_text("⚠️ Noto‘g‘ri format. Iltimos, matnni tekshirib yozing.")

async def hisobot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("⛔ Bu buyruq faqat adminlar uchun.")
        return
    user_id = update.effective_user.id
    pdf_path = generate_pdf(user_id)
    if pdf_path:
        await update.message.reply_document(document=open(pdf_path, "rb"))

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("hisobot", hisobot))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_polling()
