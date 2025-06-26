from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

# Renderda TOKEN ni Environment Variable orqali qo‘shasiz
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom, qalaysiz? 😊")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
