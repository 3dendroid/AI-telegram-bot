FROM python:3.11-slim

# set a working directory
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy your bot code
COPY telegram_mistral_bot.py .

# run the bot
CMD ["python", "bot.py"]
