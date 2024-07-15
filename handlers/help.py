from telegram import Update
from telegram.ext import CallbackContext


async def help_command(update: Update, context: CallbackContext) -> None:
    help_message = (
        "🎬 *CineMate Bot Help* 🍿\n\n"
        "/start - Welcome message\n"
        "/help - Display help message\n"
        "/genre - Browse movies by genre\n"
        "/movie <name> - Search for a specific movie"
    )
    await update.message.reply_text(help_message, parse_mode='Markdown')
