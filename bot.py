import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Railway Variables dan olinadi
TOKEN = os.getenv("BOT_TOKEN")


# ===== COMMANDLAR =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Bot ishga tushdi ✅")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start - boshlash\n/help - yordam")


# Oddiy echo (yozgan narsani qaytaradi)
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)


# ===== MAIN =====

def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN topilmadi! Railway Variables ga qo‘shing.")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
