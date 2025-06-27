from flask import Flask, request
import telegram
import os
from datetime import datetime
import random

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
URL_PATH = f"/{TOKEN}"

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)
data_store = {}
phrases = [
    "👍 Juda yaxshi ish! Yana davom eting!",
    "👏 Ajoyib! Hisobni boshqarishda davom etamiz.",
    "🤖 Bosh hisobchi sizni diqqat bilan kuzatmoqda!",
    "📈 Hisob yangilandi! Barakalla!"
]

@app.route(URL_PATH, methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    if update.message:
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        user_name = update.message.from_user.first_name
        text = update.message.text.strip()

        if user_id not in data_store:
            data_store[user_id] = []

        numbers = [float(s.replace(',', '.')) for s in text.split() if s.replace('.', '', 1).isdigit()]
        if numbers:
            amount = sum(numbers)
            name = ' '.join([w for w in text.split() if not w.replace('.', '', 1).isdigit()])
            category = ai_categorize(name)
            location = extract_location(text)
            entry = {
                "name": name.strip(),
                "amount": amount,
                "category": category,
                "location": location,
                "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            data_store[user_id].append(entry)
            reply = random.choice(phrases)
            bot.send_message(chat_id, f"🔔 {user_name}, bosh hisobchi qayd qildi: {name} - {amount} ({category}) [{location}]\n{reply}")
            send_summary_if_needed(user_id, chat_id)
        else:
            bot.send_message(chat_id, "🤖 Bosh hisobchi tushunmadi. Masalan: Non 1000 yoki 30 dori deb yozing.")
    return 'ok'

@app.route('/')
def index():
    return 'Bosh hisobchi ishga tushdi!'

def ai_categorize(text):
    if 'non' in text.lower():
        return "Oziq-ovqat"
    return "Umumiy"

def extract_location(text):
    return "Noma’lum joy"

def send_summary_if_needed(user_id, chat_id):
    if len(data_store[user_id]) % 5 == 0:
        summary = f"📊 Bosh hisobchi hisobot: Siz {len(data_store[user_id])} ta xarajat yozdingiz. Barakalla!"
        bot.send_message(chat_id, summary)
