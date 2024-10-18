import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"Received /start from {update.effective_user.username}")
    await update.message.reply_text("Salam, je suis l7erf bot, l'Ensamien qui va vous aider")

def main():
    try:
        logging.info("Initializing bot...")
        app = ApplicationBuilder().token("8088453308:AAGqgkEXVcRU0VnNIMyDY_mATnDnmuL7Zr8").build()
        app.add_handler(CommandHandler("start", start))
        logging.info("Bot is running... Waiting for commands.")
        app.run_polling()
    except Exception as e:
        logging.error(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
