# bot.py
import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

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

# --- Telegram Bot Uygulaması ---
app_tg = ApplicationBuilder().token(BOT_TOKEN).build()

# --- Komutlar ve Mesajlar ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌟 Merhaba! Karma Bot aktif. /start veya 'selam' yazabilirsin.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    if "selam" in text.lower():
        await update.message.reply_text("Selam Zeynal 🤖 Nasılsın bugün?")
    else:
        await update.message.reply_text(f"Gelen mesaj: {text}")

# --- Handler Kayıtları ---
app_tg.add_handler(CommandHandler("start", start))
app_tg.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# --- Flask Route (Render Health Check) ---
@app.route("/", methods=["GET"])
def home():
    return "Karma Bot çalışıyor 🚀"

# --- Flask Webhook (isteğe bağlı, şu anda polling aktif) ---
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), app_tg.bot)
    app_tg.update_queue.put(update)
    return "ok"

# --- Ana Çalıştırma ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info("Karma Bot başlatılıyor...")

    # Flask uygulamasını arka planda başlat
    from threading import Thread
    def run_flask():
        app.run(host="0.0.0.0", port=port)

    Thread(target=run_flask).start()

    # Telegram polling başlat
    app_tg.run_polling()
