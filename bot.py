import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.methods import DeleteWebhook
from aiogram.types import Message
from dotenv import load_dotenv
from mistralai import Mistral

# Load environment variables from .env file
load_dotenv()

# Retrieve API keys and tokens from environment
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")  # Your Mistral.ai API key
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Your Telegram bot token

# Model selection for Mistral.ai
MODEL = "mistral-small-latest"
client = Mistral(api_key=MISTRAL_API_KEY)

# In-memory dictionary to store chat history per chat ID
chat_history = {}

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Bot and Dispatcher
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


# Handler for the /start command definition
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """
    Send a greeting message when the user starts the bot.
    """
    await message.answer('Hello! I am an AI assistant powered by Mistral.ai. Send me your query.')


# Handler for any text message
@dp.message(F.text)
async def handle_text(message: Message):
    """
    Process incoming user messages, forward them and conversation history to Mistral, and return the AI's response.
    """
    chat_id = message.chat.id

    # Initialize chat history on first message
    if chat_id not in chat_history:
        chat_history[chat_id] = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            }
        ]

    # Append the user's message to history
    chat_history[chat_id].append({
        "role": "user",
        "content": message.text
    })

    # Send a chat completion request to Mistral.ai
    chat_response = client.chat.complete(
        model=MODEL,
        messages=chat_history[chat_id]
    )

    # Extract and append the assistant's reply
    assistant_text = chat_response.choices[0].message.content
    chat_history[chat_id].append({
        "role": "assistant",
        "content": assistant_text
    })

    # Limit history length to avoid context overflow
    if len(chat_history[chat_id]) > 10:
        chat_history[chat_id] = [chat_history[chat_id][0]] + chat_history[chat_id][-9:]

    # Send the AI's response back to the user
    await message.answer(assistant_text, parse_mode="Markdown")


async def main():
    """
    Configure webhook cleanup and start polling for updates.
    """
    # Remove existing webhooks and drop pending updates
    await bot(DeleteWebhook(drop_pending_updates=True))
    # Start long-polling loop
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Launch the bot
    asyncio.run(main())
