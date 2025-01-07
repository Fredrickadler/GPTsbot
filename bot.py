import os
import telebot
from flask import Flask, request

# متغیرهای محیطی
BOT_TOKEN = os.getenv("BOT_TOKEN", "8085521867:AAHf8mWjjt6Xnw0MiyxWBTVoFX_BYO71SZA")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://gptsbot.onrender.com")

# ایجاد ربات
bot = telebot.TeleBot(BOT_TOKEN)

# ایجاد سرور Flask
app = Flask(__name__)

# تنظیم Webhook
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_data = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/", methods=["GET"])
def index():
    return "Bot is running!", 200

# دستور نمونه برای ربات
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "سلام! چطور می‌توانم کمکتان کنم؟")

# راه‌اندازی Webhook
def setup_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")

if __name__ == "__main__":
    setup_webhook()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)