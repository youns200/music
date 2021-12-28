from pyrogram.types import (InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)

from hama import db_mem
from config import CHANNEL, NAMECH

join = InlineKeyboardMarkup(
    [
    [InlineKeyboardButton(text=f"{NAMECH}", url=f"{CHANNEL}")],
    ]
)
