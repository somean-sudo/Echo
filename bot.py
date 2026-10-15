import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ.get("BOT_TOKEN", "")
DB_FILE = "songs.json"


def load_songs():
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_songs(songs):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(songs, f, indent=2, ensure_ascii=False)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        song_id = context.args[0]
        if song_id.startswith("song_"):
            song_id = song_id[5:]

        song = load_songs().get(song_id)

        if song:
            keyboard = [[
                InlineKeyboardButton(
                    "⬇️ Download Full Song 🎶",
                    callback_data="get_" + song_id,
                )
            ]]
            await update.message.reply_text(
                "🎵 " + song["title"],
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        else:
            await update.message.reply_text("Song not found.")
        return

    await update.message.reply_text(
        "Echo Music 🎧\n\n"
        "Send me an audio file to save it and create a download link.\
