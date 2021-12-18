import asyncio
import os
import random
from asyncio import QueueEmpty

from pyrogram import filters
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, KeyboardButton, Message,
                            ReplyKeyboardMarkup, ReplyKeyboardRemove)

from config import get_queue
from hama import BOT_USERNAME, MUSIC_BOT_NAME, app, db_mem
from hama.Core.PyTgCalls import Queues
from hama.Core.PyTgCalls.Converter import convert
from hama.Core.PyTgCalls.Downloader import download
from hama.Core.PyTgCalls.Yukki import (pause_stream, resume_stream,
                                        skip_stream, stop_stream)
from hama.Database import (is_active_chat, is_music_playing, music_off,
                            music_on, remove_active_chat)
from hama.Decorators.admins import AdminRightsCheck
from hama.Decorators.checker import checker, checkerCB
from hama.Inline import audio_markup, primary_markup
from hama.Utilities.changers import time_to_seconds
from hama.Utilities.chat import specialfont_to_normal
from hama.Utilities.theme import check_theme
from hama.Utilities.thumbnails import gen_thumb
from hama.Utilities.timer import start_timer
from hama.Utilities.youtube import get_yt_info_id

loop = asyncio.get_event_loop()


__MODULE__ = "چاتی دەنگی"
__HELP__ = """


/pause
- بۆ ڕاگرتنی پەخشکردن.

/resume
- بۆ دەسپێکردنەوەی پەخشکردن.

/skip
- بۆ تێپەڕاندنی تراک بۆ تراکی داهاتو

/end or /stop
- بۆ وەستاندنی پەخشکردن.

/queue
- بۆ بینینی لیستی داواکراوەکان.


"""


@app.on_message(
    filters.command(["pause", "skip", "resume", "stop", "end"])
    & filters.group
)
@AdminRightsCheck
@checker
async def admins(_, message: Message):
    global get_queue
    if not len(message.command) == 1:
        return await message.reply_text("هەڵەڕوویدا لە بەکارهێنانی فرمانەکان.")
    if not await is_active_chat(message.chat.id):
        return await message.reply_text("هیچ پەخشێک لە ئارادا نیە.")
    chat_id = message.chat.id
    if message.command[0][1] == "a":
        if not await is_music_playing(message.chat.id):
            return await message.reply_text("موزیک وەستاوە.")
        await music_off(chat_id)
        await pause_stream(chat_id)
        await message.reply_text(
            f"🎧 پەخشکردن وەستا لەلایەن {message.from_user.mention}!"
        )
    if message.command[0][1] == "e":
        if await is_music_playing(message.chat.id):
            return await message.reply_text("موزیک پەخشکراوە.")
        await music_on(chat_id)
        await resume_stream(chat_id)
        await message.reply_text(
            f"🎧 پەخشکردن دەستپێکراوە لەلایەن {message.from_user.mention}!"
        )
    if message.command[0][1] == "t" or message.command[0][1] == "n":
        try:
            Queues.clear(message.chat.id)
        except QueueEmpty:
            pass
        await remove_active_chat(chat_id)
        await stop_stream(chat_id)
        await message.reply_text(
            f"🎧 چاتی دەنگی کۆتای هات لەلایەن {message.from_user.mention}!"
        )
    if message.command[0][1] == "k":
        Queues.task_done(chat_id)
        if Queues.is_empty(chat_id):
            await remove_active_chat(chat_id)
            await message.reply_text(
                "هیچ تراکێکی تر لە __ڕێزدا__ نیە \n\nیارمەتی دەر دەرچۆ لەچاتی دەنگی"
            )
           await stop_stream(chat_id)
            return
        else:
            videoid = Queues.get(chat_id)["file"]
            got_queue = get_queue.get(chat_id)
            if got_queue:
                got_queue.pop(0)
            finxx = f"{videoid[0]}{videoid[1]}{videoid[2]}"
            aud = 0
            if str(finxx) != "raw":
                mystic = await message.reply_text(
                    f"**{MUSIC_BOT_NAME} لیستی پەخشکردن**\n\n__داگرتنی لیستی پەخشکردن بۆ دواتر....__"
                )
                (
                    title,
                    duration_min,
                    duration_sec,
                    thumbnail,
                ) = get_yt_info_id(videoid)
                await mystic.edit(
                    f"**{MUSIC_BOT_NAME} دابەزاندنی**\n\n**Title:** {title[:50]}\n\n0% ▓▓▓▓▓▓▓▓▓▓▓▓ 100%"
                )
                downloaded_file = await loop.run_in_executor(
                    None, download, videoid, mystic, title
                )
                raw_path = await convert(downloaded_file)
                await skip_stream(chat_id, raw_path)
                theme = await check_theme(chat_id)
                chat_title = await specialfont_to_normal(message.chat.title)
                thumb = await gen_thumb(
                    thumbnail, title, message.from_user.id, theme, chat_title
                )
                buttons = primary_markup(
                    videoid, message.from_user.id, duration_min, duration_min
                )
                await mystic.delete()
                mention = db_mem[videoid]["username"]
                final_output = await message.reply_photo(
                    photo=thumb,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=(
                        f"<b>__تراکی داواکراو__</b>\n\n🎥<b>__دەست کرا بە پەخشکردنی:__ </b>[{title[:25]}](https://www.youtube.com/watch?v={videoid}) \n⏳<b>__کات:__</b> {duration_min} خوڵەک\n👤**__داواکراوە لەلایەن:__** {mention}"
                    ),
                )
                 os.remove(thumb)
            else:
                await skip_stream(chat_id, videoid)
                afk = videoid
                title = db_mem[videoid]["title"]
                duration_min = db_mem[videoid]["duration"]
                duration_sec = int(time_to_seconds(duration_min))
                mention = db_mem[videoid]["username"]
                videoid = db_mem[videoid]["videoid"]
                if str(videoid) == "smex1":
                    buttons = buttons = audio_markup(
                        videoid,
                        message.from_user.id,
                        duration_min,
                        duration_min,
                    )
                    thumb = "Utils/Telegram.JPEG"
                    aud = 1
                else:
                    _path_ = _path_ = (
                        (str(afk))
                        .replace("_", "", 1)
                        .replace("/", "", 1)
                        .replace(".", "", 1)
                    )
                    thumb = f"cache/{_path_}final.png"
                    buttons = primary_markup(
                        videoid,
                        message.from_user.id,
                        duration_min,
                        duration_min,
                    )
                final_output = await message.reply_photo(
                    photo=thumb,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"<b>__تراکی داواکراو__</b>\n\n🎥<b>__دۆخی ئیستا پەخشکراوە:__</b> {title} \n⏳<b>__کات:__</b> {duration_min} \n👤<b>__داواکراوە لەلایەن:__ </b> {mention}",
                )
              await start_timer(
                videoid,
                duration_min,
                duration_sec,
                final_output,
                message.chat.id,
                message.from_user.id,
                aud,
            )
