
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai
import os
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
OPENAI_API_KEY = "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"
TELEGRAM_API_TOKEN = "8085521867:AAHf8mWjjt6Xnw0MiyxWBTVoFX_BYO71SZA"

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Function to handle user messages
def handle_message(update, context):
    user_message = update.message.text  # User's message
    try:
        # Sending message to OpenAI and getting a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response['choices'][0]['message']['content']
    except Exception as e:
        reply = "An error occurred. Please try again later."
    
    update.message.reply_text(reply)  # Send reply to Telegram

# Start the bot
def main():
    updater = Updater(TELEGRAM_API_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Handle text messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Start polling
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
