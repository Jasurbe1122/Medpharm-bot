from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging
import json
import re
from datetime import datetime
from utils import parse_text
from ocr_utils import extract_text_from_image
from pdf_utils import generate_pdf_report

TOKEN = "YOUR_BOT_TOKEN"
DATA_FILE = "expenses.json"
logging.basicConfig(level=logging.INFO)

try:
    with open(DATA_FILE, "r") as f:
        expenses = json.load(f)
except:
    expenses = {}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Assalomu alaykum! Xarajatlaringizni yozing. Rasm yoki matn yuborishingiz mumkin.")

def handle_text(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)
    user_name = update.message.from_user.first_name
    text = update.message.text

    result = parse_text(text)
    if not result:
        update.message.reply_text("Hech qanday xarajat topilmadi.")
        return

    if user_id not in expenses:
        expenses[user_id] = []

    entry = {
        "name": user_name,
        "category": result["category"],
        "amount": result["amount"],
        "location": result.get("location"),
        "person": result.get("person"),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    expenses[user_id].append(entry)
    save_data()
    update.message.reply_text(f"✅ {user_name}, saqlandi: {result['category']} – {result['amount']} so'm")

def handle_photo(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)
    photo_file = update.message.photo[-1].get_file()
    image_path = f"photo_{user_id}.jpg"
    photo_file.download(image_path)

    extracted_text = extract_text_from_image(image_path)
    update.message.text = extracted_text
    handle_text(update, context)

def generate_report(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)
    user_name = update.message.from_user.first_name

    if user_id not in expenses or not expenses[user_id]:
        update.message.reply_text("Sizda hali hech qanday ma'lumot yo'q.")
        return

    path = generate_pdf_report(user_id, expenses[user_id])
    with open(path, "rb") as f:
        update.message.reply_document(document=f, filename="hisobot.pdf")

updater = Updater(token=TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("hisobot", generate_report))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
dp.add_handler(MessageHandler(Filters.photo, handle_photo))

updater.start_polling()
