import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler

from handlers.button import button
from handlers.genre import genre
from handlers.help import help_command
from handlers.movie_search import movie_search
from handlers.start import start

load_dotenv()

TOKEN = os.getenv("BOT_API_KEY")

def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("genre", genre))
    app.add_handler(CommandHandler("movie", movie_search))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()

if __name__ == '__main__':
    main()
