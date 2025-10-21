# bot.py
import os
import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters

# --- Logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Flask Uygulaması ---
app = Flask(__name__)

# --- Telegram Bot Token ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("BOT_TOKEN environment variable not found!")
    raise RuntimeError("BOT_TOKEN environment variable is required.")

bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)

# --- Komutlar ve Mesajlar ---
def start(update: Update, context):
    update.message.reply_text("🌞 Merhaba! Karma Bot aktif. /start veya 'selam' yazabilirsin.")

def echo(update: Update, context):
    text = update.message.text or ""
    if "selam" in text.lower():
        update.message.reply_text("Selam Zeynal 🤖 Nasılsın bugün?")
    else:
        update.message.reply_text(f"Gelen mesaj: {text}")

# --- Dispatcher Handler Kaydı ---
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# --- Flask Route ---
@app.route("/", methods=["GET"])
def index():
    return "Karma Bot çalışıyor 🚀"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# --- Ana Çalıştırma ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app_url = os.environ.get("RENDER_EXTERNAL_URL") or os.environ.get("APP_URL")
    if app_url:
        webhook_url = f"{app_url}/{BOT_TOKEN}"
        try:
            bot.set_webhook(webhook_url)
            logger.info(f"Webhook set to: {webhook_url}")
        except Exception as e:
            logger.exception(f"Webhook ayarlanırken hata: {e}")
    app.run(host="0.0.0.0", port=port)
fixed bot.py for Telegram karma bot
