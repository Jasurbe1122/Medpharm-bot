
from flask import Flask, request
import telegram, os
from ai_parser import parse_text
from utils import save_expense, get_summary_text
from pdf_utils import generate_pdf_report
from image_reader import extract_text_from_image
from voice_parser import convert_voice_to_text

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or "YOUR_BOT_TOKEN"
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat_id

    if update.message.text:
        text = update.message.text
        result = parse_text(text)
        save_expense(chat_id, result)
        bot.send_message(chat_id, f"✅ {result['name']} uchun {result['amount']} {result['unit']} saqlandi.")
    elif update.message.photo:
        file = update.message.photo[-1].get_file()
        text = extract_text_from_image(file.download())
        result = parse_text(text)
        save_expense(chat_id, result)
        bot.send_message(chat_id, f"📸 Rasm: {result['name']} uchun {result['amount']} {result['unit']} saqlandi.")
    elif update.message.voice:
        file = update.message.voice.get_file()
        text = convert_voice_to_text(file.download())
        result = parse_text(text)
        save_expense(chat_id, result)
        bot.send_message(chat_id, f"🔊 Ovoz: {result['name']} uchun {result['amount']} {result['unit']} saqlandi.")

    return "ok"
