import os
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from groq import Groq

# ===========================
# ENVIRONMENT VARIABLES
# ===========================

TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi!")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY topilmadi!")

client = Groq(api_key=GROQ_API_KEY)

user_languages = {}


# ===========================
# START
# ===========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["🇺🇿 O'zbekcha"],
        ["🇷🇺 Русский"],
        ["🇬🇧 English"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "🌍 Tilni tanlang / Choose language:",
        reply_markup=reply_markup
    )


# ===========================
# CHAT
# ===========================

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text
    user_id = update.message.from_user.id

    if user_text == "🇺🇿 O'zbekcha":
        user_languages[user_id] = "O'zbekcha"
        await update.message.reply_text("✅ O'zbek tili tanlandi.")
        return

    if user_text == "🇷🇺 Русский":
        user_languages[user_id] = "Русский"
        await update.message.reply_text("✅ Русский язык выбран.")
        return

    if user_text == "🇬🇧 English":
        user_languages[user_id] = "English"
        await update.message.reply_text("✅ English selected.")
        return

    language = user_languages.get(user_id, "O'zbekcha")

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": f"""
Sen Jasurbek yaratgan AI yordamchisan.

Javob tili: {language}

Qoidalar:
- Aniq va tushunarli javob ber.
- Grammatik xato qilma.
- Hozirgi yil 2026.
- Bilmagan narsani uydirma qilma.
- Foydalanuvchiga hurmat bilan javob ber.
- Agar "Seni kim yaratgan?" deb so'rasa:
"Meni Jasurbek yaratgan. Men uning AI yordamchi loyihasiman." deb javob ber.
"""
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ]
        )

        answer = response.choices[0].message.content

        emoji = random.choice(
            ["🤖", "✨", "💡", "🚀", "✅"]
        )

        await update.message.reply_text(
            f"{emoji} {answer}"
        )

    except Exception as e:
        await update.message.reply_text(
            f"❌ Xatolik:\n{e}"
        )


# ===========================
# MAIN
# ===========================

def main():

    app = Application.builder().token(
        TELEGRAM_BOT_TOKEN
    ).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            chat
        )
    )

    print("✅ Bot ishga tushdi...")

    app.run_polling()


if __name__ == "__main__":
    main()