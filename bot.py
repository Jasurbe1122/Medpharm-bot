from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os

# .env fayldan tokenni o‘qish
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # ← tokenni .env fayldan oladi

# /start komandasi uchun javob
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom, qalaysiz? 😊")

# Asosiy ishga tushirish funksiyasi
def main():
    app = Application.builder().token(TOKEN).build()  # ← mana bu yerda
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

# Botni ishga tushirish
if __name__ == "__main__":
    main()
