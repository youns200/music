from config import MUSIC_BOT_NAME, SUPPORT_CHANNEL, SUPPORT_GROUP, CHANNEL, NAMECH
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)

from hama import BOT_USERNAME


def start_pannel():
    if not SUPPORT_CHANNEL and not SUPPORT_GROUP and CHANNEL and NAMECH:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 فرمانەکان", url="https://telegra.ph/Ozan-Music-Bot-02-28"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔧 ڕێکخستن", callback_data="settingm"
                )
            ],
         [
                InlineKeyboardButton(
                    text=f"{NAMECH}", url=f"{CHANNEL}"
                ),
            ],
        ]
        return f"🎛  ** {MUSIC_BOT_NAME}**", buttons
    if not SUPPORT_CHANNEL and SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 فرمانەکان", url="https://telegra.ph/Ozan-Music-Bot-02-28"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔧 ڕێکخستن", callback_data="settingm"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📨گروپی پگشیری", url=f"{SUPPORT_GROUP}"
                ),
            ],
        ]
        return f"🎛  ** {MUSIC_BOT_NAME}*", buttons
    if SUPPORT_CHANNEL and not SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 فرمانەکان", url="https://telegra.ph/Ozan-Music-Bot-02-28"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔧 ڕێکخستن", callback_data="settingm"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📨کەنالی پگشیری", url=f"{SUPPORT_CHANNEL}"
                ),
            ],
                   [
                InlineKeyboardButton(
                    text=f"{NAMECH}", url=f"{CHANNEL}"
                ),
            ],
        ]
        return f"🎛  ** {MUSIC_BOT_NAME}**", buttons
    if SUPPORT_CHANNEL and SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 فرمانەکان", url="https://telegra.ph/Ozan-Music-Bot-02-28"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔧 ڕێکخستن", callback_data="settingm"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📨کەنالی پگشیری", url=f"{SUPPORT_CHANNEL}"
                ),
                InlineKeyboardButton(
                    text="📨گروپی پگشیری", url=f"{SUPPORT_GROUP}"
                ),
            ],
                   [
                InlineKeyboardButton(
                    text=f"{NAMECH}", url=f"{CHANNEL}"
                ),
            ],
        ]
        return f"🎛  **This is {MUSIC_BOT_NAME}**", buttons


def private_panel():
    if not SUPPORT_CHANNEL and not SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 فرمانەکان", url="https://telegra.ph/Ozan-Music-Bot-02-28"
                ),
            ],
            [
                InlineKeyboardButton(
                    "➕زیادم بکە بۆ گروپ چاتەکەت",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ],
                   [
                InlineKeyboardButton(
                    text=f"{NAMECH}", url=f"{CHANNEL}"
                ),
            ],
        ]
        return f"🎛  ** {MUSIC_BOT_NAME}**", buttons
    if not SUPPORT_CHANNEL and SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 فرمانەکان", url="https://telegra.ph/Amort-Music-Bot-12-13"
                ),
            ],
            [
                InlineKeyboardButton(
                    "➕ زیادم بکە بۆ گروپ چاتەکەت",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📨گروپی پگشیری", url=f"{SUPPORT_GROUP}"
                ),
            ],
                   [
                InlineKeyboardButton(
                    text=f"{NAMECH}", url=f"{CHANNEL}"
                ),
            ],
        ]
        return f"🎛  ** {MUSIC_BOT_NAME}*", buttons
    if SUPPORT_CHANNEL and not SUPPORT_GROUP and CHANNEL and NAMECH:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 فرمانەکان", url="https://telegra.ph/Amort-Music-Bot-12-13"
                ),
            ],
            [
                InlineKeyboardButton(
                    "➕ زیادم بکە بۆ گروپ چاتەکەت",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📨کەنالی پگشیری", url=f"{SUPPORT_CHANNEL}"
                ),
            ],
[
                InlineKeyboardButton(
                    text=f"{NAMECH}", url=f"{CHANNEL}"
                ),
            ],
        ]
        return f"🎛  ** {MUSIC_BOT_NAME}**", buttons
    if SUPPORT_CHANNEL and SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 فرمانەکان", url="https://telegra.ph/Ozan-Music-Bot-02-28"
                ),
            ],
            [
                InlineKeyboardButton(
                    "➕ زیادم بکە بۆ گروپ چاتەکەت",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📨کەنالی پگشیری", url=f"{SUPPORT_CHANNEL}"
                ),
                InlineKeyboardButton(
                    text="📨گروپی پگشیری", url=f"{SUPPORT_GROUP}"
                ),
            ],
[
                InlineKeyboardButton(
                    text=f"{NAMECH}", url=f"{CHANNEL}"
                ),
            ],
        ]
        return f"🎛  ** {MUSIC_BOT_NAME}**", buttons


def setting_markup():
    buttons = [
        [
            InlineKeyboardButton(text="🔈 کوالێتی دەنگ", callback_data="AQ"),
            InlineKeyboardButton(text="🎚 قەبارەی دەنگ هاتن", callback_data="AV"),
        ],
        [
            InlineKeyboardButton(
                text="👥 ڕێگەپێدراوەکان", callback_data="AU"
            ),
            InlineKeyboardButton(
                text="💻 زانیاریەکان", callback_data="Dashboard"
            ),
        ],
        [
            InlineKeyboardButton(text="✖️ داخستن", callback_data="close"),
            InlineKeyboardButton(text="🔙 گەرانەوە", callback_data="okaybhai"),
        ],
[
                InlineKeyboardButton(
                    text=f"{NAMECH}", url=f"{CHANNEL}"
                ),
            ],
    ]
    return f"🔧  **{MUSIC_BOT_NAME} ڕێبەندەکان**", buttons


def volmarkup():
    buttons = [
        [
            InlineKeyboardButton(
                text="🔄 پێش ڕێکخستن 🔄", callback_data="HV"
            )
        ],
        [
            InlineKeyboardButton(text="🔈 نزم", callback_data="LV"),
            InlineKeyboardButton(text="🔉 مامناوەندی", callback_data="MV"),
        ],
        [
            InlineKeyboardButton(text="🔊 بەرز", callback_data="HV"),
            InlineKeyboardButton(text="🔈 گەورەکراو", callback_data="VAM"),
        ],
        [
            InlineKeyboardButton(
                text="🔽 خواستیار 🔽", callback_data="Custommarkup"
            )
        ],
        [InlineKeyboardButton(text="🔙 گەرانەوە", callback_data="settingm")],
               [
                InlineKeyboardButton(
                    text=f"{NAMECH}", url=f"{CHANNEL}"
                ),
            ],
    ]
    return f"🔧  **{MUSIC_BOT_NAME} ڕێبەندەکان**", buttons


def custommarkup():
    buttons = [
        [
            InlineKeyboardButton(text="+10", callback_data="PTEN"),
            InlineKeyboardButton(text="-10", callback_data="MTEN"),
        ],
        [
            InlineKeyboardButton(text="+25", callback_data="PTF"),
            InlineKeyboardButton(text="-25", callback_data="MTF"),
        ],
        [
            InlineKeyboardButton(text="+50", callback_data="PFZ"),
            InlineKeyboardButton(text="-50", callback_data="MFZ"),
        ],
        [InlineKeyboardButton(text="🔼خواستیار 🔼", callback_data="AV")],
               [
                InlineKeyboardButton(
                    text=f"{NAMECH}", url=f"{CHANNEL}"
                ),
            ],
    ]
    return f"🔧  **{MUSIC_BOT_NAME} ڕێبەندەکان**", buttons


def usermarkup():
    buttons = [
        [
            InlineKeyboardButton(text="👥 هەموکەس", callback_data="EVE"),
            InlineKeyboardButton(text="🙍 بەڕێوەبەرەکان", callback_data="AMS"),
        ],
        [
            InlineKeyboardButton(
                text="📋 لیستی بەکارهێنەرە ڕێگەپێدراوەکان", callback_data="USERLIST"
            )
        ],
        [InlineKeyboardButton(text="🔙 گەرانەوە", callback_data="settingm")],
               [
                InlineKeyboardButton(
                    text=f"{NAMECH}", url=f"{CHANNEL}"
                ),
            ],
    ]
    return f"🔧  **{MUSIC_BOT_NAME} ڕێبەندەکان**", buttons


def dashmarkup():
    buttons = [
        [
            InlineKeyboardButton(text="✔️ کاتی نوێکاری", callback_data="UPT"),
            InlineKeyboardButton(text="💾 رام", callback_data="RAT"),
        ],
        [
            InlineKeyboardButton(text="💻 کوب", callback_data="CPT"),
            InlineKeyboardButton(text="💽 دیسک", callback_data="DIT"),
        ],
        [InlineKeyboardButton(text="🔙 گەرانەوە", callback_data="settingm")],
               [
                InlineKeyboardButton(
                    text=f"{NAMECH}", url=f"{CHANNEL}"
                ),
            ],
    ]
    return f"🔧  **{MUSIC_BOT_NAME} ڕێبەندەکان **", buttons
