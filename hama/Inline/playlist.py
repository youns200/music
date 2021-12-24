from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)
from config import CHANNEL, NAMECH

def check_markup(user_name, user_id, videoid):
    buttons = [
        [ 
          
         InlineKeyboardButton(
                text=f"chek",
                callback_data=f"playlist_check {user_id}|Group|{videoid}",
            ),
            InlineKeyboardButton(
                text=f"🎶گروپ لیست",
                callback_data=f"playlist_check {user_id}|Group|{videoid}",
            ),
            InlineKeyboardButton(
                text=f"🔣{user_name[:8]} لیست",
                callback_data=f"playlist_check {user_id}|Personal|{videoid}",
            ),
        ],
        [InlineKeyboardButton(text="🗑 ", callback_data="close"),
         InlineKeyboardButton(
                    text=f"{NAMECH}", url=f"{CHANNEL}"
                ),
            ],
    ]
    return buttons


def playlist_markup(user_name, user_id, videoid):
    buttons = [
        [
            InlineKeyboardButton(
                text=f"🎶گروپ لیست",
                callback_data=f"show_genre {user_id}|Group|{videoid}",
            ),
            InlineKeyboardButton(
                text=f"🔣{user_name[:8]} لیست ",
                callback_data=f"show_genre {user_id}|Personal|{videoid}",
            ),
        ],
        [InlineKeyboardButton(text="🗑 ", callback_data="close"),
                InlineKeyboardButton(
                    text=f"{NAMECH}", url=f"{CHANNEL}"
                ),
            ],
    ]
    return buttons


def play_genre_playlist(user_id, type, videoid):
    buttons = [
        [InlineKeyboardButton(text=f"🔁دەستپێکردنی پەخشکردن",callback_data=f"play_playlist {user_id}|{type}|Punjabi",),
            InlineKeyboardButton(
                text="⬅️ گەرانەوە",
                callback_data=f"main_playlist {videoid}|{type}|{user_id}",)],
               [InlineKeyboardButton(text=f"{NAMECH}", url=f"{CHANNEL}")],
    ]
    return buttons


def add_genre_markup(user_id, type, videoid):
    buttons = [
        [
            InlineKeyboardButton(
                text=f"✚ بەڵێ",
                callback_data=f"add_playlist {videoid}|{type}|Punjabi",
            ),
            InlineKeyboardButton(
                text=f"➖ نەخێر",
                callback_data=f"goback {videoid}|{user_id}",
            ),
        ],
       
               [
                InlineKeyboardButton(
                    text=f"{NAMECH}", url=f"{CHANNEL}"
                ),
            ],
    ]
    return buttons


def check_genre_markup(type, videoid, user_id):
    buttons = [
        [
          
            InlineKeyboardButton(
                text=f"پەخشکردن",
                callback_data=f"check_playlist {type}|Punjabi",
            ),
            InlineKeyboardButton(
                text=f"نەخێر", callback_data=f"close"
            ),
        ],   
      [
      InlineKeyboardButton(
                    text=f"{NAMECH}", url=f"{CHANNEL}"
                ),
            ],
    ]
    return buttons


def third_playlist_markup(user_name, user_id, third_name, userid, videoid):
    buttons = [
        [
            InlineKeyboardButton(
                text=f"🎶گروپ لیست",
                callback_data=f"show_genre {user_id}|Group|{videoid}",
            ),
            InlineKeyboardButton(
                text=f"{user_name[:8]} لیستی",
                callback_data=f"show_genre {user_id}|Personal|{videoid}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"{third_name[:16]} لیستی",
                callback_data=f"show_genre {userid}|third|{videoid}",
            ),
        ],
        [InlineKeyboardButton(text="🗑 داخستن", callback_data="close")],
               [
                InlineKeyboardButton(
                    text=f"{NAMECH}", url=f"{CHANNEL}"
                ),
            ],
    ]
    return buttons


def paste_queue_markup(url):
    buttons = [
        [
            InlineKeyboardButton(text="▶️", callback_data=f"resumecb"),
            InlineKeyboardButton(text="⏸️", callback_data=f"pausecb"),
            InlineKeyboardButton(text="⏭️", callback_data=f"skipcb"),
            InlineKeyboardButton(text="⏹️", callback_data=f"stopcb"),
        ],
        [InlineKeyboardButton(text="پشکنینی لیستی پەخشکردن", url=f"{url}")],
        [InlineKeyboardButton(text="🗑 داخستن", callback_data=f"close"),
         InlineKeyboardButton(
                    text=f"{NAMECH}", url=f"{CHANNEL}"
                ),
            ],
      
    ]
    return buttons


def fetch_playlist(user_name, type, genre, user_id, url):
    buttons = [
        [
            InlineKeyboardButton(
                text=f"پەخشکردنی {user_name[:10]} {genre} لیستی",
                callback_data=f"play_playlist {user_id}|{type}|{genre}",
            ),
        ],
        [InlineKeyboardButton(text="لیستی پەخشکردن", url=f"{url}")],
        [InlineKeyboardButton(text="🗑 داخستن", callback_data=f"close")],
               [
                InlineKeyboardButton(
                    text=f"{NAMECH}", url=f"{CHANNEL}"
                ),
            ],
    ]
    return buttons


def delete_playlist_markuup(type, genre):
    buttons = [
        [
            InlineKeyboardButton(
                text=f"بەلێ! سڕینەوە",
                callback_data=f"delete_playlist {type}|{genre}",
            ),
            InlineKeyboardButton(text="نەخێر!", callback_data=f"close"),
        ],
               [
                InlineKeyboardButton(
                    text=f"{NAMECH}", url=f"{CHANNEL}"
                ),
            ],
    ]
    return buttons
