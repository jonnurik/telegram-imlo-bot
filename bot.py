import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot ishlayapti ✅")


# HAR QANDAY MATN
async def check_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "xato" in text or "yomon" in text:
        await update.message.reply_text("❌ Iltimos, xato so‘z ishlatmang!")

    print("Kelgan matn:", text)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # 👇 ENG MUHIM
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_text))

    app.run_polling()


if __name__ == "__main__":
    main()
