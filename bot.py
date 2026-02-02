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
    raise ValueError("BOT_TOKEN environment variable topilmadi!")


# =========================
# SPELLCHECKER (50k lug'at)
# =========================
spell = SpellChecker(language=None)
spell.word_frequency.load_text_file("uzbek_50k_dictionary.txt")


# =========================
# PRIVATE /start
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot faqat guruhda ishlaydi.")


# =========================
# SMART CHECK (1 ta eng yaxshi tuzatish)
# =========================
async def check_text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message or not update.message.text:
        return

    # faqat group
    if update.effective_chat.type == "private":
        return

    text = update.message.text.lower()
    words = re.findall(r"[a-zʻ’']+", text)

    mistakes = spell.unknown(words)

    # xato yo'q → jim
    if not mistakes:
        return

    best_word = None
    best_fix = None
    best_score = 999

    # 🔥 ENG MUHIM QISM
    # eng kichik tahrir masofali (eng mantiqiy) tuzatishni tanlaymiz
    for w in mistakes:
        fix = spell.correction(w)

        if not fix:
            continue

        distance = abs(len(w) - len(fix))  # oddiy kontekst ball

        if distance < best_score:
            best_score = distance
            best_word = w
            best_fix = fix

    if best_word:
        await update.message.reply_text(f"❌ {best_word} → {best_fix}")


# =========================
# MAIN
# =========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start, filters=filters.ChatType.PRIVATE))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.ChatType.GROUPS,
            check_text
        )
    )

    print("Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
