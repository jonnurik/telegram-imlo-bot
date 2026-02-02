import os
import re
from spellchecker import SpellChecker
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

spell = SpellChecker()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot ishlayapti. Matn yuboring.")


async def check_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    words = re.findall(r"[A-Za-z']+", text.lower())

    mistakes = spell.unknown(words)

    if not mistakes:
        return

    msg = "❌ Xato so‘zlar:\n"

    for w in mistakes:
        sug = ", ".join(list(spell.candidates(w))[:3])
        msg += f"\n{w} → {sug}"

    await update.message.reply_text(msg)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_text))

    print("Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
