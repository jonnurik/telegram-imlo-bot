
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from spellchecker import SpellChecker

TOKEN = os.getenv("BOT_TOKEN")

spell = SpellChecker(language=None)

# Load Uzbek dictionary
with open("uz_words.txt", "r", encoding="utf-8") as f:
    spell.word_frequency.load_words(f.read().split())

async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().split()
    mistakes = spell.unknown(text)

    if mistakes:
        reply = []
        for word in mistakes:
            correction = spell.correction(word)
            reply.append(f"❌ {word} → ✅ {correction}")
        await update.message.reply_text("\n".join(reply))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Imlo tekshiruvchi bot ishga tushdi ✅")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_message))

app.run_polling()
