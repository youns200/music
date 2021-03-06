from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)
from config import NAMECH, CHANNEL

def song_markup(videoid, duration, user_id, query, query_type):
    buttons = [
        [
            InlineKeyboardButton(
                text="❮",
                callback_data=f"song_right B|{query_type}|{query}|{user_id}",
            ),
            InlineKeyboardButton(
                text="⬇️ داگرتن",
                callback_data=f"qwertyuiopasdfghjkl {videoid}|{user_id}",
            ),
            InlineKeyboardButton(
                text="❯",
                callback_data=f"song_right F|{query_type}|{query}|{user_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🗑 ",
                callback_data=f"forceclose {query}|{user_id}",
            ),
               
                InlineKeyboardButton(
                    text=f"{NAMECH}", url=f"{CHANNEL}"
                ),
            ],
    ]
    return buttons


def song_download_markup(videoid, user_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="⬇️ داگرتنی گۆرانی",
                callback_data=f"gets audio|{videoid}|{user_id}",
            ),
            InlineKeyboardButton(
                text="⬇️ داگرتنی ڤیدیۆ",
                callback_data=f"gets video|{videoid}|{user_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🗑 ",
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
                InlineKeyboardButton(
                    text=f"{NAMECH}", url=f"{CHANNEL}"
                ),
            ],
    ]
    return buttons
#new
def download_markup(videoid, user_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="⬇️ داگرتنی گۆرانی",
                callback_data=f"gets audio|{videoid}|{user_id}",
            ),
            InlineKeyboardButton(
                text="⬇️ داگرتنی ڤیدیۆ",
                callback_data=f"gets video|{videoid}|{user_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⬅️ گەرانەوە", callback_data=f"goback {videoid}|{user_id}"
            ),
            InlineKeyboardButton(text="🗑 داخستن", callback_data=f"close"),
        ],
      [InlineKeyboardButton(text=f"{NAMECH}", url=f"{CHANNEL}")],
    ]
    return buttons
