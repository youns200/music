import os
import time
from datetime import datetime

import psutil
from pyrogram import Client, filters
from pyrogram.types import Message

from hama import BOT_USERNAME, MUSIC_BOT_NAME, app, boottime
from hama.Utilities.ping import get_readable_time

__MODULE__ = "پینگ"
__HELP__ = """

/ping - بپشکنە ئەگەر بۆت زیندووە یان نا .
"""


async def bot_sys_stats():
    bot_uptime = int(time.time() - boottime)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    stats = f"""
Uptime: {get_readable_time((bot_uptime))}
کوپ: {cpu}%
ڕام: {mem}%
دیسک: {disk}%"""
    return stats


@app.on_message(filters.command(["ping", f"ping@{BOT_USERNAME}"]))
async def ping(_, message):
    start = datetime.now()
    response = await message.reply_photo(
        photo="https://telegra.ph/file/676cc67c8acd8e35954b1.jpg",
        caption=">> Pong!",
    )
    uptime = await bot_sys_stats()
    end = datetime.now()
    resp = (end - start).microseconds / 1000
    await response.edit_text(
        f"**Pong!**\n`⚡{resp} ms`\n\n<b><u>{MUSIC_BOT_NAME} ئامارەکانی سیستەم:</u></b>{uptime}"
    )
