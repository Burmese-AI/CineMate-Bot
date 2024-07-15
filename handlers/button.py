from telegram import Update
from telegram.ext import CallbackContext

from api import fetch_movies


async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    genre_id = query.data

    await query.answer()

    movies = fetch_movies(genre_id)
    if movies:
        message = "Good choice! 🍿 Here are the top 10 movies of your selected genre:\n\n"

        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=message,
            parse_mode='Markdown'
        )
        for movie in movies:
            caption = (
                f"🎬 *{movie['title']}* ({movie['release_year']})\n\n"
                f"📝 *Storyline*\n\n"
                f"{movie['overview']}\n\n"
                f"⭐ IMDb Rating: {movie['rating']:.1f}"
            )
            if movie['poster_url']:
                await context.bot.send_photo(
                    chat_id=query.message.chat_id,
                    photo=movie['poster_url'],
                    caption=caption,
                    parse_mode='Markdown'
                )
            else:
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text=caption,
                    parse_mode='Markdown'
                )
    else:
        await query.edit_message_text(text="Failed to fetch movies. Please try again later.")
