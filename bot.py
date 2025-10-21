import os
from flask import Flask, request
import telegram

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telegram.Bot(token=BOT_TOKEN)

@app.route('/')
def home():
    return "Karma Bot aktif 🎯"

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    message = update.message.text

    if message.lower() == "/start":
        bot.sendMessage(chat_id=chat_id, text="Merhaba 👋 Karma Bot aktif! Komutları deneyebilirsin.")
    elif "selam" in message.lower():
        bot.sendMessage(chat_id=chat_id, text="Selam Zeynal 👀 Nasılsın bugün?")
    else:
        bot.sendMessage(chat_id=chat_id, text=f"Gelen mesaj: {message}")

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
