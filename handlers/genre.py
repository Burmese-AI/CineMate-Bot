from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from api import fetch_genres


async def genre(update: Update, context: CallbackContext) -> None:
    genres = fetch_genres()
    if genres:
        keyboard = [
            InlineKeyboardButton(genre_name, callback_data=str(genre_id))
            for genre_id, genre_name in genres.items()
        ]
        keyboard_chunks = [keyboard[i:i + 2] for i in range(0, len(keyboard), 2)]

        markup = InlineKeyboardMarkup(keyboard_chunks)
        await update.message.reply_text(
            'What genre are you in the mood for? 🍿 Select a genre below to see the top ten movies of that genre.',
            reply_markup=markup
        )
    else:
        await update.message.reply_text('Failed to fetch genres. Please try again later.')
