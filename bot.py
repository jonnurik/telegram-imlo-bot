import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from openai import OpenAI


TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

if not TOKEN:
    raise ValueError("BOT_TOKEN topilmadi")

if not OPENAI_KEY:
    raise ValueError("OPENAI_API_KEY topilmadi")

client = OpenAI(api_key=OPENAI_KEY)


# =========================
# AI tekshiruvchi funksiya
# =========================
async def ai_check(sentence: str):

    prompt = f"""
Quyidagi o‘zbek gapni tekshir.
Agar xato bo‘lsa faqat 1 ta eng muhim xatoni chiqar.

Format:
xato → togri

Agar xato bo‘lmasa:
OK

Gap: {sentence}
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return res.choices[0].message.content.strip()


# =========================
# /start (private)
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot faqat guruhlarda ishlaydi.")


# =========================
# group xabar tekshirish
# =========================
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # faqat group
    if update.effective_chat.type == "private":
        return

    text = update.message.text

    result = await ai_check(text)

    if result == "OK":
        return

    await update.message.reply_text(f"❌ {result}")


# =========================
# main
# =========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check))

    print("AI bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
