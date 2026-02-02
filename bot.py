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

# Spell checker
spell = SpellChecker()


# -------------------------
# START
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Imlo tekshiruvchi bot ishlayapti!\n\n"
        "Matn yuboring — xato so‘zlarni tekshiraman."
    )


# -------------------------
# TEXT CHECKER
# -------------------------
async def check_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # faqat lotin harflarni ajratamiz
    words = re.findall(r"[A-Za-z']+", text.lower())

    if not words:
        return

    mistakes = spell.unknown(words)

    if not mistakes:
        return

    reply = "❌ Xato so‘zlar:\n\n"

    for w in mistakes:
        suggestions = spell.candidates(w)
        sug = ", ".join(list(suggestions)[:3])
        reply += f"• {w} → {sug}\n"

    await update.message.reply_text(reply)


# -------------------------
# MAIN
# -------------------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # private + group ishlashi uchun
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, check_text)
    )

    print("Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
