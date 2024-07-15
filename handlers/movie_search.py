from telegram import Update
from telegram.ext import CallbackContext

from api import search_movies


async def movie_search(update: Update, context: CallbackContext) -> None:
    if context.args:
        movie_name = " ".join(context.args)
        movies = search_movies(movie_name)
        if movies:
            for movie in movies:
                caption = (
                    f"🎬 *{movie['title']}* ({movie['release_year']})\n\n"
                    f"📝 *Storyline*\n\n"
                    f"{movie['overview']}\n\n"
                    f"⭐ IMDb Rating: {movie['rating']:.1f}"
                )
                if movie['poster_url']:
                    await context.bot.send_photo(
                        chat_id=update.message.chat_id,
                        photo=movie['poster_url'],
                        caption=caption,
                        parse_mode='Markdown'
                    )
                else:
                    await context.bot.send_message(
                        chat_id=update.message.chat_id,
                        text=caption,
                        parse_mode='Markdown'
                    )
        else:
            await update.message.reply_text('No movies found with that name. Please try another name.')
    else:
        await update.message.reply_text('Please provide a movie name to search.')
