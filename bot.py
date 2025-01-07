import os
import telebot
import openai

# Load environment variables from config.txt
with open("config.txt") as f:
    config = {}
    for line in f:
        key, value = line.strip().split("=", 1)
        config[key] = value

# Initialize APIs
BOT_TOKEN = config["BOT_TOKEN"]
OPENAI_API_KEY = config["OPENAI_API_KEY"]

openai.api_key = OPENAI_API_KEY
bot = telebot.TeleBot(BOT_TOKEN)

# Handle "/start" command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! من اینجا هستم تا به سوالات شما پاسخ بدهم. فقط سوال خود را تایپ کنید.")

# Handle user messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Send user message to OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        
        # Get the AI's reply
        reply = response['choices'][0]['message']['content']
        
        # Send the reply back to the user
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"مشکلی پیش آمد: {e}")

# Polling
bot.polling()