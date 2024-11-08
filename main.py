import os
import logging
from dotenv import load_dotenv  # Load .env variables
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import openai  # Import OpenAI

# Load the .env file to access the API keys
load_dotenv()

# Get the API keys from the environment variables
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set up logging to track events and errors
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Respond to the /start command."""
    logging.info(f"Received /start from {update.effective_user.username}")
    await update.message.reply_text("Salam, je suis l7erf bot, l'Ensamien qui va vous aider")

async def summarize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Summarize the text from a PDF (example command)."""
    logging.info(f"Received /summarize from {update.effective_user.username}")
    
    # Example text for summarization
    text_to_summarize = "Your PDF content goes here."

    openai.api_key = OPENAI_API_KEY  # Set OpenAI API key

    # Call OpenAI's summarization model (example)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Summarize this: {text_to_summarize}"}]
    )

    # Extract and send the summary
    summary = response['choices'][0]['message']['content']
    await update.message.reply_text(summary)

def main():
    try:
        logging.info("Initializing bot...")
        
        # Use the loaded token to build the application
        app = ApplicationBuilder().token(TELEGRAM_API_KEY).build()
        
        # Add command handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("summarize", summarize))  # Add summarize command
        
        logging.info("Bot is running... Waiting for commands.")
        # Start polling for updates
        app.run_polling()
    except Exception as e:
        logging.error(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
