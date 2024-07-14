import os

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
)

from api import fetch_genres, fetch_movies, search_movies

load_dotenv()

TOKEN = os.getenv("BOT_API_KEY")

async def start(update: Update, context: CallbackContext) -> None:
    message = (
        f"🎬 Welcome to CineMate, {update.effective_user.first_name}! 🍿\n\n"
        "I'm here to help you discover great movies. "
        "Enjoy your movie journey!"
    )
    await update.message.reply_text(message)


async def help_command(update: Update, context: CallbackContext) -> None:
    help_message = (
        "🎬 *CineMate Bot Help* 🍿\n\n"
        "/start - Welcome message\n"
        "/help - Display help message\n"
        "/genre - Browse movies by genre\n"
        "/movie "
        "<name> - Search for a specific movie"
    )
    await update.message.reply_text(help_message, parse_mode='Markdown')


async def genre(update: Update, context: CallbackContext) -> None:
    genres = fetch_genres()
    if genres:
        keyboard = [
            InlineKeyboardButton(genre_name, callback_data=str(genre_id))
            for genre_id, genre_name in genres.items()
		]
        keyboard_chunks = [keyboard[i:i + 2] for i in range(0, len(keyboard), 2)]

        markup = InlineKeyboardMarkup(keyboard_chunks)
        await update.message.reply_text('What genre are you in the mood for? 🍿 Select a genre below to see the top ten movies of that genre.', reply_markup=markup)
    else:
        await update.message.reply_text('Failed to fetch genres. Please try again later.')


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
