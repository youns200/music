from typing import Dict, List, Union

from pyrogram import Client, filters

from hama import BOT_USERNAME, MUSIC_BOT_NAME, app, db
from hama.Database import _get_theme, get_theme, save_theme
from hama.Decorators.permission import PermissionCheck

themes = [
    "Random",
]

__MODULE__ = "Theme"
__HELP__ = """
/settheme
- Set a theme for thumbnails.
/theme
- Check Theme for your chat.
"""


@app.on_message(
    filters.command(["settheme", f"settheme@{BOT_USERNAME}"]) & filters.group
)
async def settheme(_, message):
    usage = f"ئەمە بابەتێک نییە.\n\nلێیان دیاریبکە\n{' | '.join(themes)}\n'Random' بەکاربهێنە بۆ بەدەستهێنانی هەڵبژاردنی هەڕەمەکی بابەتەکان"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    theme = message.text.split(None, 1)[1].strip()
    if theme not in themes:
        return await message.reply_text(usage)
    note = {
        "theme": theme,
    }
    await save_theme(message.chat.id, "theme", note)
    await message.reply_text(f"**بەسەرکەوتوی وێنە بچوکەکە گۆرا بۆ ** {theme}")

