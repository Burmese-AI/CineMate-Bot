from telegram import Update
from telegram.ext import CallbackContext


async def start(update: Update, context: CallbackContext) -> None:
    message = (
        f"🎬 Welcome to CineMate, {update.effective_user.first_name}! 🍿\n\n"
        "I'm here to help you discover great movies. "
        "Enjoy your movie journey!"
    )
    await update.message.reply_text(message)
