from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)

from hama import db_mem
from config import CHANNEL, NAMECH

def url_markup(videoid, duration, user_id, query, query_type):
    buttons = [
        [
            InlineKeyboardButton(
                text="❮",
                callback_data=f"slider B|{query_type}|{query}|{user_id}",
            ),
            InlineKeyboardButton(
                text="🎵",
                callback_data=f"hama {videoid}|{duration}|{user_id}",
            ),
            InlineKeyboardButton(
                text="❯",
                callback_data=f"slider F|{query_type}|{query}|{user_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔎 ئەنجامی زیاتر",
                callback_data=f"Search {query}|{user_id}",
            ),
            InlineKeyboardButton(
                text="🗑 داخستنی گەران",
                callback_data=f"forceclose {query}|{user_id}",
            ),
        ],
        [InlineKeyboardButton(text=f"{NAMECH}", url=f"{CHANNEL}"),],
    ]
    return buttons


def url_markup2(videoid, duration, user_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="🎵",
                callback_data=f"hama {videoid}|{duration}|{user_id}",
            ),
            InlineKeyboardButton(
                text="🗑",
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
      [InlineKeyboardButton(text=f"{NAMECH}", url=f"{CHANNEL}")],
    ]
    return buttons


def search_markup(
    ID1,
    ID2,
    ID3,
    ID4,
    ID5,
    duration1,
    duration2,
    duration3,
    duration4,
    duration5,
    user_id,
    query,
):
    buttons = [
        [
            InlineKeyboardButton(
                text="1️⃣", callback_data=f"hama {ID1}|{duration1}|{user_id}"
            ),
            InlineKeyboardButton(
                text="2️⃣", callback_data=f"hama {ID2}|{duration2}|{user_id}"
            ),
            InlineKeyboardButton(
                text="3️⃣", callback_data=f"hama {ID3}|{duration3}|{user_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="4️⃣", callback_data=f"hama {ID4}|{duration4}|{user_id}"
            ),
            InlineKeyboardButton(
                text="5️⃣", callback_data=f"hama {ID5}|{duration5}|{user_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="<", callback_data=f"popat 1|{query}|{user_id}"
            ),
            InlineKeyboardButton(
                text="🗑", callback_data=f"forceclose {query}|{user_id}"
            ),
            InlineKeyboardButton(
                text=">", callback_data=f"popat 1|{query}|{user_id}"
            ),
        ],
      [InlineKeyboardButton(text=f"{NAMECH}", url=f"{CHANNEL}")],
    ]
    return buttons


def search_markup2(
    ID6,
    ID7,
    ID8,
    ID9,
    ID10,
    duration6,
    duration7,
    duration8,
    duration9,
    duration10,
    user_id,
    query,
):
    buttons = [
        [
            InlineKeyboardButton(
                text="6️⃣",
                callback_data=f"hama2 {ID6}|{duration6}|{user_id}",
            ),
            InlineKeyboardButton(
                text="7️⃣",
                callback_data=f"hama2 {ID7}|{duration7}|{user_id}",
            ),
            InlineKeyboardButton(
                text="8️⃣",
                callback_data=f"hama2 {ID8}|{duration8}|{user_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="9️⃣",
                callback_data=f"hama2 {ID9}|{duration9}|{user_id}",
            ),
            InlineKeyboardButton(
                text="🔟",
                callback_data=f"hama2 {ID10}|{duration10}|{user_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="<", callback_data=f"popat 2|{query}|{user_id}"
            ),
            InlineKeyboardButton(
                text="🗑", callback_data=f"forceclose {query}|{user_id}"
            ),
            InlineKeyboardButton(
                text=">", callback_data=f"popat 2|{query}|{user_id}"
            ),
        ],
       [InlineKeyboardButton(text=f"{NAMECH}", url=f"{CHANNEL}")],
    ]
    return buttons


def secondary_markup(videoid, user_id):
    buttons = [
        [
            InlineKeyboardButton(text="▶️", callback_data=f"resumecb"),
            InlineKeyboardButton(text="⏸️", callback_data=f"pausecb"),
            InlineKeyboardButton(text="⏭️", callback_data=f"skipcb"),
            InlineKeyboardButton(text="⏹️", callback_data=f"stopcb"),
        ],
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
            InlineKeyboardButton(text="🗑 داخستن", callback_data=f"close"),
       InlineKeyboardButton(text=f"{NAMECH}", url=f"{CHANNEL}")],
    ]
    return buttons


def primary_markup(videoid, user_id, current_time, total_time):
    if videoid not in db_mem:
        db_mem[videoid] = {}
    db_mem[videoid]["check"] = 2
    buttons = [
        [
            InlineKeyboardButton(
                text=f"{total_time} ------------------ {current_time}",
                callback_data=f"timer_checkup_markup {videoid}|{user_id}",
            )
        ],
        [
            InlineKeyboardButton(text="▶️", callback_data=f"resumecb"),
            InlineKeyboardButton(text="⏸️", callback_data=f"pausecb"),
            InlineKeyboardButton(text="⏭️", callback_data=f"skipcb"),
            InlineKeyboardButton(text="⏹️", callback_data=f"stopcb"),
        ],
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
            InlineKeyboardButton(text="🗑 داخستن", callback_data=f"close"),
            InlineKeyboardButton(text=f"{NAMECH}", url=f"{CHANNEL}")],
    ]
    return buttons


def timer_markup(videoid, user_id, current_time, total_time):
    buttons = [
        [
            InlineKeyboardButton(
                text=f"{total_time} ------------------ {current_time}",
                callback_data=f"timer_checkup_markup {videoid}|{user_id}",
            )
        ],
        [
            InlineKeyboardButton(text="▶️", callback_data=f"resumecb"),
            InlineKeyboardButton(text="⏸️", callback_data=f"pausecb"),
            InlineKeyboardButton(text="⏭️", callback_data=f"skipcb"),
            InlineKeyboardButton(text="⏹️", callback_data=f"stopcb"),
        ],
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
            InlineKeyboardButton(text="🗑 داخستن", callback_data=f"close"),
            InlineKeyboardButton(text=f"{NAMECH}", url=f"{CHANNEL}")],
    ]
    return buttons


def audio_markup(videoid, user_id, current_time, total_time):
    if videoid not in db_mem:
        db_mem[videoid] = {}
    db_mem[videoid]["check"] = 2
    buttons = [
        [
            InlineKeyboardButton(text="▶️", callback_data=f"resumecb"),
            InlineKeyboardButton(text="⏸️", callback_data=f"pausecb"),
            InlineKeyboardButton(text="⏭️", callback_data=f"skipcb"),
            InlineKeyboardButton(text="⏹️", callback_data=f"stopcb"),
        ],
        [InlineKeyboardButton(text="🗑 داخستن", callback_data=f"close"),
         InlineKeyboardButton(text=f"{NAMECH}", url=f"{CHANNEL}")],
    ]
    return buttons


def audio_timer_markup_start(videoid, user_id, current_time, total_time):
    buttons = [
        [
            InlineKeyboardButton(text="▶️", callback_data=f"resumecb"),
            InlineKeyboardButton(text="⏸️", callback_data=f"pausecb"),
            InlineKeyboardButton(text="⏭️", callback_data=f"skipcb"),
            InlineKeyboardButton(text="⏹️", callback_data=f"stopcb"),
        ],
        [InlineKeyboardButton(text="🗑 داخستن", callback_data=f"close")],
      [InlineKeyboardButton(text=f"{NAMECH}", url=f"{CHANNEL}")],
    ]
    return buttons

  
audio_markup2 = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="▶️", callback_data=f"resumecb"),
            InlineKeyboardButton(text="⏸️", callback_data=f"pausecb"),
            InlineKeyboardButton(text="⏭️", callback_data=f"skipcb"),
            InlineKeyboardButton(text="⏹️", callback_data=f"stopcb"),
        ],
        [InlineKeyboardButton("🗑 داخستن", callback_data="close"),
         InlineKeyboardButton(text=f"{NAMECH}", url=f"{CHANNEL}")],
    ]
)
#nwe
def welcome = InlineKeyboardMarkup(
     [
        [InlineKeyboardButton(text=f"{NAMECH}", url=f"{CHANNEL}")],
      ]
    )
    return buttons
