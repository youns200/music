import asyncio
import json

from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message

from hama import SUDOERS, app,
from hama.Database import get_gbans_count, get_served_chats, get_sudoers


@app.on_message(filters.command("stats") & ~filters.edited)
async def gstats(_, message):
    served_chats = []
        chats = await get_served_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
        blocked = await get_gbans_count()
        sudoers = await get_sudoers()
        j = 0
        for count, user_id in enumerate(sudoers, 0):
            try:
                user = await app.get_users(user_id)
                j += 1
            except Exception:
                continue
        smex = f"""
[•]<u>**Bot Stats**</u>
**سزادراوەکان:** {blocked}
**بەڕێوەبەرەکان:** {j}
**گرووپەکان:** {len(served_chats)}"""
    await message.reply_text(smex)
    return
