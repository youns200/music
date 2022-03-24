import asyncio
import importlib
import os
import re

from config import LOG_GROUP_ID
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from rich.console import Console
from rich.table import Table
from youtubesearchpython import VideosSearch

from hama import (ASSID, ASSMENTION, ASSNAME, ASSUSERNAME, BOT_ID, BOT_NAME, CHANNEL, NAMECH, 
                   BOT_USERNAME, SUDOERS, app, db, pymongodb, userbot, MUST_JOIN)
from hama.Core.Logger.Log import (startup_delete_last, startup_edit_last,
                                   startup_send_new)
from hama.Core.PyTgCalls.hama import run
from hama.Database import get_active_chats, get_sudoers, remove_active_chat, is_served_user, add_served_user
from hama.Inline import private_panel
from hama.Plugins import ALL_MODULES
from hama.Utilities.inline import paginate_modules

loop = asyncio.get_event_loop()



@app.on_message(filters.command("start") & filters.private)
async def start_command(_, message):
    user_id = message.from_user.id
    if await is_served_user(user_id):
        pass
    else:
        await add_served_user(user_id)
        return
    if len(message.text.split()) > 1:
        name = (message.text.split(None, 1)[1]).lower()
        if name[0] == "s":
            sudoers = await get_sudoers()
            text = "**__لیستی بەڕێوەبەرەکانی بۆت:-__**\n\n"
            j = 0
            for count, user_id in enumerate(sudoers, 1):
                try:
                    user = await app.get_users(user_id)
                    user = (
                        user.first_name if not user.mention else user.mention
                    )
                except Exception:
                    continue
                text += f"➤ {user}\n"
                j += 1
            if j == 0:
                await message.reply_text("بەڕێوەبەر زیادنەکراون")
            else:
                await message.reply_text(text)
        if name == "help":
            text, keyboard = await help_parser(message.from_user.mention)
            await message.delete()
            return await app.send_text(
                message.chat.id,
                text,
                reply_markup=keyboard,
            )
        if name[0] == "i":
            m = await message.reply_text("🔎 دۆزینەوەی زانیاری!")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in results.result()["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = f"""
🔍__**زانیاری تراکی ئەم ڤیدیۆ**__

❇️**ناو:** {title}

⏳**کات:** {duration} خوڵەکە
👀**بینەر:** `{views}`
⏰**کات بڵاووەکراو:** {published}
🎥**ناوی کەناڵ:** {channel}
📎**بەستەرەی کەناڵ:** [ئێرە دابگرە]({channellink})
🔗**بەستەرەی ڤیدیۆ:** [Link]({link})
"""
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🎥 بینینی ڤیدیۆ", url=f"{link}"
                        ),
                        InlineKeyboardButton(
                            text="🔄 ", callback_data="close"
                        ),
                    ],
                ]
            )
            await m.delete()
            return await app.send_photo(
                message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                parse_mode="markdown",
                reply_markup=key,
            ) 
    out = private_panel()
    return await app.send_audio(
                message.chat.id,
                audio="https://t.me/chawakannt/4",
                caption= """♨️ لە ڕێگای ئەم بۆتەوە دەتوانی گۆرانی و مۆسیقا و قورئان پەخش بکەی لە ڤۆیس چاتی گروپەکەت

📝هەموو فەرمانەکانی بۆت دانراوە لە دگمەی فەرمانەکان بیان دەۆزەرەوە و بەباشی کۆنتڕۆلی بۆت بکە""",
                parse_mode="markdown",
        reply_markup=InlineKeyboardMarkup(out[1]),
    )


if __name__ == "__main__":
    loop.run_until_complete(initiate_bot())
