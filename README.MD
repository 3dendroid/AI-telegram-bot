# Telegram AI Bot with Mistral.ai

A stateful Telegram chatbot powered by Mistral.ai.  
Maintains per-chat conversation history, calls the Mistral chat-completion API, and replies in real time.

## Structure:

```
my-telegram-bot/
├── telegram_mistral_bot.py
├── requirements.txt
├── .env              # local development only
└── Dockerfile or Procfile        # optional
```

## Features

- ✅ **Persistent Chat Memory**  
  Keeps a rolling window of the last 10 messages per chat so the assistant “remembers” context.
- 🤖 **Mistral.ai Integration**  
  Uses the `mistralai` Python SDK to call Mistral’s chat-completion endpoint.
- ⚡ **Fast & Lightweight**  
  Built with [Aiogram](https://docs.aiogram.dev/) for high-performance async polling.
- 🛠️ **Easy Deployment**  
  Ready to deploy on Railway (Docker or plain Python).

## Tech Stack

- **Python 3.10+**
- **Aiogram** — async Telegram Bot API client
- **mistralai** — Mistral.ai SDK for chat completions
- **python-dotenv** — loads `.env` files in development
- **Redis** (optional) or in-memory dict for short-term history
