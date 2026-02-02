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

if not TOKEN:
    raise ValueError("BOT_TOKEN topilmadi")


# =========================
# SPELLCHECKER (offline)
# =========================
spell = SpellChecker(language=None)
spell.word_frequency.load_text_file("uzbek_50k_dictionary.txt")


# =========================
# /start
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Imlo bot ishlayapti (bepul offline).")


# =========================
# GROUP CHECK
# =========================
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.lower()

    words = re.findall(r"[a-zʻ’']+", text)

    mistakes = spell.unknown(words)

    if not mistakes:
        return  # jim

    wrong = list(mistakes)[0]
    correct = spell.correction(wrong)

    await update.message.reply_text(f"❌ {wrong} → {correct}")


# =========================
# MAIN
# =========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start, filters=filters.ChatType.PRIVATE))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.ChatType.GROUPS,
            check
        )
    )

    print("Bepul imlo bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
