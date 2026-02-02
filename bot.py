import os
import logging
import language_tool_python
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

# Uzbek (latin) spell checker
tool = language_tool_python.LanguageTool('ru-RU')  # Uzbek yo‘q → rus eng yaqin
# agar inglizcha ko‘proq bo‘lsa → en-US


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Imlo tekshiruvchi bot ishga tushdi ✅")


async def check_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    matches = tool.check(text)

    if not matches:
        return  # xato yo‘q → jim

    corrected = language_tool_python.utils.correct(text, matches)

    await update.message.reply_text(
        f"❌ Xatolik topildi:\n\n"
        f"✍️ Siz: {text}\n"
        f"✅ To‘g‘risi: {corrected}"
    )


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, check_text)
    )

    app.run_polling()


if __name__ == "__main__":
    main()
