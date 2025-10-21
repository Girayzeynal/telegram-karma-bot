# bot.py
import os
import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Bot token'ı Render üzerinde environment variable olarak ekle: BOT_TOKEN
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("BOT_TOKEN environment variable is not set.")
    raise RuntimeError("BOT_TOKEN environment variable is required.")

bot = Bot(token=BOT_TOKEN)

# Dispatcher - burada workers=0 (senkron) kullanıyoruz; webhook ile uygun çalışır
dispatcher = Dispatcher(bot, None, use_context=True)

# Handler'lar
def start(update, context):
    update.message.reply_text("Merhaba 👋 Karma Bot aktif. Komutları denemek için /start yazabilirsin.")

def echo_reply(update, context):
    text = update.message.text or ""
    # Basit kelime bazlı cevap örnekleri
    if text.lower() == "selam":
        update.message.reply_text("Selam Zeynal 👋 Nasılsın bugün?")
    else:
        update.message.reply_text(f"Gelen mesaj: {text}")

# Kayıt
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo_reply))

# Basit ana sayfa
@app.route('/', methods=['GET'])
def index():
    return "Karma Bot is up. Use webhook to send updates."

# Webhook path: /<BOT_TOKEN>
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    # Telegram'dan gelen JSON -> Update objesine çevirir
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

if __name__ == "__main__":
    # Render ve benzeri ortamlarda PORT env var kullanılır
    port = int(os.environ.get("PORT", "5000"))

    # Render kendi dış URL'sini RENDER_EXTERNAL_URL olarak sağlar -- varsa webhook'u otomatik ayarla
    app_url = os.environ.get("RENDER_EXTERNAL_URL") or os.environ.get("APP_URL")  # Render için RENDER_EXTERNAL_URL ideal
    if app_url:
        webhook_url = f"{app_url}/{BOT_TOKEN}"
        try:
            bot.set_webhook(webhook_url)
            logger.info("Webhook set to: %s", webhook_url)
        except Exception as e:
            logger.exception("Webhook setlerken hata oldu: %s", e)

    app.run(host="0.0.0.0", port=port)
