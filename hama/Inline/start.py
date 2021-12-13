
from config import MUSIC_BOT_NAME, SUPPORT_CHANNEL, SUPPORT_GROUP, CC
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)

from hama import BOT_USERNAME

def setting_markup2():
    buttons = [
        [
            InlineKeyboardButton(text="🔈 کواڵێیتی دەنگ", callback_data="AQ"),
            InlineKeyboardButton(text="🎚 قەبارەی دەنگ", callback_data="AV"),
        ],
        [
            InlineKeyboardButton(
                text="👥 بەکارهێنەرانی تایبەت", callback_data="AU"
            ),
            InlineKeyboardButton(
                text="💻 ئامارەکان", callback_data="Dashboard"
            ),
        ],
        [
            InlineKeyboardButton(text="✖️ داخستن", callback_data="close"),
        ],
    ]
    return f"🔧  **{MUSIC_BOT_NAME} ڕێکخستنی**", buttons



def start_pannel():
    if not SUPPORT_CHANNEL and not SUPPORT_GROUP and CC:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 فرمانەکان و یارمەتی", url=f"{CC}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔧 ڕێکخستن", callback_data="settingm"
                )
            ],
        ]
        return f"🎛  **ئەمە {MUSIC_BOT_NAME}**", buttons
    if not SUPPORT_CHANNEL and SUPPORT_GROUP and CC:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 فرمانەکان و یارمەتی", url=f"{CC}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔧 Settings", callback_data="settingm"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📨گروپی پشگیری", url=f"{SUPPORT_GROUP}"
                ),
            ],
        ]
        return f"🎛  **ئەمە {MUSIC_BOT_NAME}*", buttons
    if SUPPORT_CHANNEL and not SUPPORT_GROUP and CC:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 فرمانەکان و یارمەتی", url=f"{CC}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔧 ڕێکخستن", callback_data="settingm"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📨کەناڵی پگشیری", url=f"{SUPPORT_CHANNEL}"
                ),
            ],
        ]
        return f"🎛  **ئەمە {MUSIC_BOT_NAME}**", buttons
    if SUPPORT_CHANNEL and SUPPORT_GROUP and CC:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 فرمانەکان و یارمەتی", url=f"{CC}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔧 ڕێکخستن", callback_data="settingm"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📨کەناڵی پگشیری ", url=f"{SUPPORT_CHANNEL}"
                ),
                InlineKeyboardButton(
                    text="📨گروپی پگشیری ", url=f"{SUPPORT_GROUP}"
                ),
            ],
        ]
        return f"🎛  **ئەمە {MUSIC_BOT_NAME}**", buttons


def private_panel():
    if not SUPPORT_CHANNEL and not SUPPORT_GROUP and CC:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 فرمانەکان و یارمەتی", url=f"{CC}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "➕ زیادی گروپم بکە",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ],
        ]
        return f"🎛  **ئەمە {MUSIC_BOT_NAME}**", buttons
    if not SUPPORT_CHANNEL and SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 فرمانەکان و یارمەتی", url=f"{CC}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "➕ زیادی گروپم بکە",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📨گروپی پگشیری", url=f"{SUPPORT_GROUP}"
                ),
            ],
        ]
        return f"🎛  **ئەمە {MUSIC_BOT_NAME}*", buttons
    if SUPPORT_CHANNEL and not SUPPORT_GROUP and CC:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 فرمانەکان و یارمەتی", url=f"{CC}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "➕ زیادی گروپم بکە",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📨کەناڵی پشگیری", url=f"{SUPPORT_CHANNEL}"
                ),
            ],
        ]
        return f"🎛  **ئەمە {MUSIC_BOT_NAME}**", buttons
    if SUPPORT_CHANNEL and SUPPORT_GROUP and CC:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 فرمانەکان و یارمەتی", url=f"{CC}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "➕ زیادی گروپم بکە",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📨کەناڵی پگشیری", url=f"{SUPPORT_CHANNEL}"
                ),
                InlineKeyboardButton(
                    text="📨گروپی پشگیری", url=f"{SUPPORT_GROUP}"
                ),
            ],
        ]
        return f"🎛  **ئەمە {MUSIC_BOT_NAME}**", buttons


def setting_markup():
    buttons = [
        [
            InlineKeyboardButton(text="🔈 کواڵێتی دەنگ", callback_data="AQ"),
            InlineKeyboardButton(text="🎚 قەبارەی دەنگ", callback_data="AV"),
        ],
        [
            InlineKeyboardButton(
                text="👥 بەکارهێنەری تایبەت", callback_data="AU"
            ),
            InlineKeyboardButton(
                text="💻 ئامارەکان", callback_data="Dashboard"
            ),
        ],
        [
            InlineKeyboardButton(text="✖️ داخستن", callback_data="close"),
            InlineKeyboardButton(text="🔙 گەرانەوە", callback_data="hamo1"),
        ],
    ]
    return f"🔧  **{MUSIC_BOT_NAME} ڕێکخستن**", buttons


def volmarkup():
    buttons = [
        [
            InlineKeyboardButton(
                text="🔄 ڕێستات کردنەوەی دەنگ 🔄", callback_data="HV"
            )
        ],
        [
            InlineKeyboardButton(text="🔈 Low Vol", callback_data="LV"),
            InlineKeyboardButton(text="🔉 Medium Vol", callback_data="MV"),
        ],
        [
            InlineKeyboardButton(text="🔊 High Vol", callback_data="HV"),
            InlineKeyboardButton(text="🔈 Amplified Vol", callback_data="VAM"),
        ],
        [
            InlineKeyboardButton(
                text="🔽 Custom Volume 🔽", callback_data="Custommarkup"
            )
        ],
        [InlineKeyboardButton(text="🔙 Go back", callback_data="settingm")],
    ]
    return f"🔧  **{MUSIC_BOT_NAME} Settings**", buttons


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
        [InlineKeyboardButton(text="🔼Custom Volume 🔼", callback_data="AV")],
    ]
    return f"🔧  **{MUSIC_BOT_NAME} Settings**", buttons


def usermarkup():
    buttons = [
        [
            InlineKeyboardButton(text="👥 هەموکەس", callback_data="EVE"),
            InlineKeyboardButton(text="🙍 بەڕێوەبەر", callback_data="AMS"),
        ],
        [
            InlineKeyboardButton(
                text="📋 لیستی بەکارهێنەرانی تایبەت", callback_data="USERLIST"
            )
        ],
        [InlineKeyboardButton(text="🔙 گەڕانەوە", callback_data="settingm")],
    ]
    return f"🔧  **{MUSIC_BOT_NAME} ڕێکخستن**", buttons


def dashmarkup():
    buttons = [
        [
            InlineKeyboardButton(text="✔️ Uptime", callback_data="UPT"),
            InlineKeyboardButton(text="💾 Ram", callback_data="RAT"),
        ],
        [
            InlineKeyboardButton(text="💻 Cpu", callback_data="CPT"),
            InlineKeyboardButton(text="💽 Disk", callback_data="DIT"),
        ],
        [InlineKeyboardButton(text="🔙 گەڕانەوە", callback_data="settingm")],
    ]
    return f"🔧  **{MUSIC_BOT_NAME} ڕێکخستن**", buttons
