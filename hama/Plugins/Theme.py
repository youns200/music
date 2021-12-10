from typing import Dict, List, Union

from pyrogram import Client, filters

from hama import BOT_USERNAME, MUSIC_BOT_NAME, app, db
from hama.Database import _get_theme, get_theme, save_theme
from hama.Decorators.permission import PermissionCheck

themes = [
    "blue",
    "black",
    "red",
    "green",
    "grey",
    "orange",
    "pink",
    "yellow",
    "Random",
]

themes2 = [
    "blue",
    "black",
    "red",
    "green",
    "grey",
    "orange",
    "pink",
    "yellow",
]

__MODULE__ = "ڕووکار"
__HELP__ = """
/settheme
- بۆ گۆڕینی ڕووکاری وێنەی سەر پەخشکردن.
/theme
- بۆ گۆڕینی ڕووکاری وێنەی سەر پەخشکردن لەگرووپەکەت.
"""


@app.on_message(
    filters.command(["settheme", f"settheme@{BOT_USERNAME}"]) & filters.group
)
async def settheme(_, message):
    usage = f"یەکێک لەم ڕووکانە هەڵبژێرە.\n\nڕووکارەکان\n{' | '.join(themes)}\n\nهەر یەکێک لەم ڕووکارانە هەڵبژێریت ڕووکاری پەخشکردن ئەگۆڕێ بۆی"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    theme = message.text.split(None, 1)[1].strip()
    if theme not in themes:
        return await message.reply_text(usage)
    note = {
        "theme": theme,
    }
    await save_theme(message.chat.id, "theme", note)
    await message.reply_text(f"ڕووکاری پەخشکردن گۆرا بۆ {theme}")


@app.on_message(filters.command("theme"))
@PermissionCheck
async def theme_func(_, message):
    await message.delete()
    _note = await get_theme(message.chat.id, "theme")
    if not _note:
        theme = "Random"
    else:
        theme = _note["theme"]
    await message.reply_text(
        f"**{MUSIC_BOT_NAME} ڕوکاری بۆتی**\n\n**روکارەی هەڵبژێراوە:-** {theme}\n\n**ڕوکارە بەردەستەکان:-** {' | '.join(themes2)} \n\nبە فەرمانی /settheme دەتوانیت بگۆڕیت."
    )

