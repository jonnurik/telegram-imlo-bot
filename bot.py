import os
import asyncio
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

client = OpenAI(api_key=OPENAI_KEY)


# =========================
# AI check (async-safe)
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

    loop = asyncio.get_event_loop()

    res = await loop.run_in_executor(
        None,
        lambda: client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
    )

    return res.choices[0].message.content.strip()


# =========================
# start (private)
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot faqat guruhlarda ishlaydi.")


# =========================
# group only handler
# =========================
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):

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

    # start faqat private
    app.add_handler(CommandHandler("start", start, filters=filters.ChatType.PRIVATE))

    # 🔥 FAQAT GROUP
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.ChatType.GROUPS,
            check
        )
    )

    print("AI bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
