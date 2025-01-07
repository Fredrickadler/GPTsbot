import os
import telebot
from flask import Flask, request

# Load configuration
with open("config.txt") as f:
    config = {}
    for line in f:
        key, value = line.strip().split("=", 1)
        config[key] = value

BOT_TOKEN = config["BOT_TOKEN"]
WEBHOOK_URL = config["WEBHOOK_URL"]

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Handle "/start" command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! من اینجا هستم تا به سوالات شما پاسخ بدهم. فقط سوال خود را تایپ کنید.")

# Handle user messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        bot.reply_to(message, f"شما گفتید: {message.text}")
    except Exception as e:
        bot.reply_to(message, f"مشکلی پیش آمد: {e}")

# Webhook route
@app.route(f"/{BOT_TOKEN}", methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

# Set webhook
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + f"/{BOT_TOKEN}")
    app.run(host="0.0.0.0", port=int(config.get("PORT", 5000)))