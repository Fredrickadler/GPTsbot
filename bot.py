import os
import telebot
import openai
from flask import Flask, request

# Load configuration
with open("config.txt") as f:
    config = {}
    for line in f:
        key, value = line.strip().split("=", 1)
        config[key] = value

BOT_TOKEN = config["BOT_TOKEN"]
WEBHOOK_URL = config["WEBHOOK_URL"]
PORT = int(config["PORT"])

# Initialize bot and OpenAI API key
bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = "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"

# Flask app for webhook
app = Flask(__name__)

# Handle "/start" command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! من یک هوش مصنوعی هستم. هر سوالی دارید بپرسید!")

# Handle user messages and connect to OpenAI
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        user_input = message.text  # Get user input

        # Send input to OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",  # یا gpt-3.5-turbo برای پاسخ‌های بهتر
            prompt=user_input,
            max_tokens=200,
            n=1,
            stop=None,
            temperature=0.7
        )

        # Send AI-generated response back to user
        bot.reply_to(message, response.choices[0].text.strip())
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
    app.run(host="0.0.0.0", port=PORT)