import telebot
import openai
import os
from flask import Flask, request

# خواندن مقادیر از فایل محیطی .env
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 5000))

# تنظیم توکن‌های مورد نیاز
bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# اپلیکیشن Flask برای وب‌هوک
app = Flask(__name__)

# تعریف یک دستور ساده
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "سلام! من اینجا هستم تا به شما کمک کنم.")

# تعریف هوش مصنوعی برای سوالات
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message.text}
            ]
        )
        bot.reply_to(message, response['choices'][0]['message']['content'])
    except Exception as e:
        bot.reply_to(message, f"خطایی رخ داد: {str(e)}")

# تنظیم وب‌هوک
@app.route(f"/{BOT_TOKEN}", methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200

@app.route("/", methods=['GET'])
def index():
    return "ربات شما در حال اجرا است!", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")
    app.run(host="0.0.0.0", port=PORT)