from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)

from hama import db_mem
from config import CHANNEL, NAMECH

def others_markup(videoid, user_id):
    if videoid not in db_mem:
        db_mem[videoid] = {}
    db_mem[videoid]["check"] = 1
    buttons = [
        [
            InlineKeyboardButton(
                text="⬇️ داگرتنی ڤیدیۆ و گۆرانی",
                callback_data=f"audio_video_download {videoid}|{user_id}",
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ گەرانەوە",
                callback_data=f"pr_go_back_timer {videoid}|{user_id}",
            ),
            InlineKeyboardButton(
                text="🗑 داخستن",
                callback_data=f"close",
            )
        ],
              [InlineKeyboardButton(text=f"{NAMECH}", url=f"{CHANNEL}")],
    ]
    return buttons


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
