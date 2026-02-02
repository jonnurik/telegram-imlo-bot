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

# ==============================
# TOKEN
# ==============================
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable topilmadi!")


# ==============================
# SPELLCHECKER (O'zbek lug‘at)
# ==============================
spell = SpellChecker(language=None)

# 🔥 siz yuklagan fayl shu yerda o‘qiladi
spell.word_frequency.load_text_file("uzbek_50k_dictionary.txt")


# ==============================
# COMMAND: /start
# ==============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Bot ishlayapti.\nMatn yuboring — imlo xatolarini tekshiraman."
    )


# ==============================
# TEXT CHECKER
# ==============================
async def check_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower()

    # faqat so‘zlarni ajratib olish
    words = re.findall(r"[a-zʻ’']+", text)

    mistakes = spell.unknown(words)

    if not mistakes:
        await update.message.reply_text("✅ Xatolar topilmadi")
        return

    msg = "❌ Xato so‘zlar:\n"

    for w in mistakes:
        suggestions = list(spell.candidates(w))[:3]
        sug = ", ".join(suggestions)
        msg += f"\n{w} → {sug}"

    await update.message.reply_text(msg)


# ==============================
# MAIN
# ==============================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_text))

    print("Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
