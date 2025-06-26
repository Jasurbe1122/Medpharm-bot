from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

# Tokenni Render ichidagi "Environment Variable" orqali olamiz
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom, qalaysiz? 😊")

# Botni ishga tushirish
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
