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
# O'zbek lug‘at
# =========================
spell = SpellChecker(language=None)
spell.word_frequency.load_text_file("uzbek_50k_dictionary.txt")


# =========================
# /start
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot faqat guruhlarda ishlaydi.")


# =========================
# GROUP CHECKER (BEPUl)
# =========================
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.lower()

    words = re.findall(r"[a-zʻ’']+", text)

    mistakes = spell.unknown(words)

    if not mistakes:
        return  # jim

    # faqat 1 ta eng yaqin xato
    wrong = list(mistakes)[0]
    correct = spell.correction(wrong)

    await update.message.reply_text(f"❌ {wrong} → {correct}")


# =========================
# main
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

    print("Bepul imlo bot ishga tushdi
