import asyncio
import os
import random
from asyncio import QueueEmpty

from config import get_queue
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputAudioStream, InputStream

from hama import BOT_USERNAME, MUSIC_BOT_NAME, app, db_mem, userbot
from hama.Core.PyTgCalls import Queues, hama
from hama.Core.PyTgCalls.Converter import convert
from hama.Core.PyTgCalls.Downloader import download

from hama.Database.queue import (add_active_chat, is_active_chat,
                                  is_music_playing, music_off, music_on,
                                  remove_active_chat)
from hama.Decorators.admins import AdminRightsCheckCB
from hama.Decorators.checker import checkerCB
from hama.Inline import (audio_markup, audio_markup2, download_markup, primary_markup)
from hama.Utilities.changers import time_to_seconds
from hama.Utilities.chat import specialfont_to_normal
from hama.Utilities.paste import isPreviewUp, paste_queue
from hama.Utilities.thumbnails import gen_thumb
from hama.Utilities.timer import start_timer
from hama.Utilities.youtube import get_yt_info_id

loop = asyncio.get_event_loop()


@app.on_callback_query(filters.regex("forceclose"))
async def forceclose(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    query, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "ڕێگەت پێنەدراوە ئەمە دابخەیت.", show_alert=True
        )
    await CallbackQuery.message.delete()
    await CallbackQuery.answer()


@app.on_callback_query(
    filters.regex(pattern=r"^(pausecb|skipcb|stopcb|resumecb|mute|unmute)$")
)
@AdminRightsCheckCB
@checkerCB
async def admin_risghts(_, CallbackQuery):
    global get_queue
    command = CallbackQuery.matches[0].group(1)
    if not await is_active_chat(CallbackQuery.message.chat.id):
        return await CallbackQuery.answer(
            "هیچ شتێک لە قسەکردنی دەنگیدا نییە.", show_alert=True
        )
    chat_id = CallbackQuery.message.chat.id
    if command == "pausecb":
        if not await is_music_playing(chat_id):
            return await CallbackQuery.answer(
                "مۆسیقا هەرئێستا وەستاوە", show_alert=True
            )
        await music_off(chat_id)
        await hama.pytgcalls.pause_stream(chat_id)
        await CallbackQuery.message.reply_text(
            f"🎧 چاتێکی دەنگی وەستاوە لەلایەن {CallbackQuery.from_user.mention}!",
            reply_markup=audio_markup2,
        )
        await CallbackQuery.message.delete()
        await CallbackQuery.answer("وەستاوە", show_alert=True)
    if command == "resumecb":
        if await is_music_playing(chat_id):
            return await CallbackQuery.answer(
                "مۆسیقا هەرئێستا دەستپێکراوە.", show_alert=True
            )
        await music_on(chat_id)
        await hama.pytgcalls.resume_stream(chat_id)
        await CallbackQuery.message.reply_text(
            f"🎧 دەنگی چات دەستی پێکردەوە لەلایەن {CallbackQuery.from_user.mention}!",
            reply_markup=audio_markup2,
        )
        await CallbackQuery.message.delete()
        await CallbackQuery.answer("دەستی پێکردەوە", show_alert=True)
    if command == "mute":
        if not await is_music_playing(chat_id):
            return await CallbackQuery.answer("ℹ️ یارمەتی دەر کپکرا.", show_alert=True)
                return
            await hama.pytgcalls.mute_stream(chat_id)
            await music_off(chat_id)
            await CallbackQuery.message.reply_text(
            f"🎧 یارمەتی دەر لە کپکرا لەلایەن {CallbackQuery.from_user.mention}!",
            reply_markup=audio_markup2,
        )
        await CallbackQuery.message.delete()
        await CallbackQuery.answer("❌ هیچ پەخێشک نیە", show_alert=True)
     if command == "unmute":
        if await is_music_playing(chat_id):
            return await CallbackQuery.answer("ℹ️ یاری دەرپێشتر لەکپکراوی لادراوە.", show_alert=True)
                return
            await hama.pytgcalls.unmute_stream(chat_id)
            await music_on(chat_id)
            await CallbackQuery.message.reply_text(
            f"🎧 یارمەتی دەر لە کپکراوی لادرا {CallbackQuery.from_user.mention}!",
            reply_markup=audio_markup2,
        )
        await CallbackQuery.message.delete()
        await CallbackQuery.answer("❌ هیچ پەخشێک نیە", show_alert=True)

     if command == "stopcb":
        try:
            Queues.clear(chat_id)
        except QueueEmpty:
            pass
        await remove_active_chat(chat_id)
        await hama.pytgcalls.leave_group_call(chat_id)
        await userbot.leave_chat(chat_id)
        await CallbackQuery.message.reply_text(
            f"🎧 دەنگی چات کۆتایی پێ هات لەلایەن {CallbackQuery.from_user.mention}!",
            reply_markup=audio_markup2,
        )
        await CallbackQuery.message.delete()
        await CallbackQuery.answer("کۆتایی پێ هات", show_alert=True)
    if command == "skipcb":
        Queues.task_done(chat_id)
        if Queues.is_empty(chat_id):
            await remove_active_chat(chat_id)
            await CallbackQuery.message.reply_text(
                f"چیتر مۆسیقا نیە لە __ ڕیز __ \n\nجێهێشتنی دەنگی چات . دوگمەی بەکارهێنراو لەلایەن :- {CallbackQuery.from_user.mention}"
            )
            await hama.pytgcalls.leave_group_call(chat_id)
            await CallbackQuery.message.delete()
            await CallbackQuery.answer(
                "بە لێشاوی چیتر مۆسیقا لە ڕیزدا نیە", show_alert=True
            )
            return
        else:
            videoid = Queues.get(chat_id)["file"]
            got_queue = get_queue.get(CallbackQuery.message.chat.id)
            if got_queue:
                got_queue.pop(0)
            finxx = f"{videoid[0]}{videoid[1]}{videoid[2]}"
            aud = 0
            if str(finxx) != "raw":
                await CallbackQuery.message.delete()
                await CallbackQuery.answer(
                    "داگرتنی گۆرانی تێپڕێندراوو....", show_alert=True
                )
                mystic = await CallbackQuery.message.reply_text(
                    f"**{MUSIC_BOT_NAME} کرداری لیستی پەخشکردن**\n\n__داگرتنی مۆسیقای داهاتوو لە لیستی پەخشکردن....__\n\nدوگمەی بەکارهێنراو لەلایەن :- {CallbackQuery.from_user.mention}"
                )
                (
                    title,
                    duration_min,
                    duration_sec,
                    thumbnail,
                ) = get_yt_info_id(videoid)
                await mystic.edit(
                    f"**{MUSIC_BOT_NAME} داگرتنی**\n\n**ناونیشان:** {title[:50]}\n\n0% ▓▓▓▓▓▓▓▓▓▓▓▓ 100%"
                )
                downloaded_file = await loop.run_in_executor(
                    None, download, videoid, mystic, title
                )
                raw_path = await convert(downloaded_file)
                await hama.pytgcalls.change_stream(
                    chat_id,
                    InputStream(
                        InputAudioStream(
                            raw_path,
                        ),
                    ),
                )
                chat_title = await specialfont_to_normal(
                    CallbackQuery.message.chat.title
                )
                thumb = await gen_thumb(
                    thumbnail,
                    title,
                    CallbackQuery.from_user.id,
                    chat_title,
                )
                buttons = primary_markup(
                    videoid,
                    CallbackQuery.from_user.id,
                    duration_min,
                    duration_min,
                )
                await mystic.delete()
                mention = db_mem[videoid]["username"]
                final_output = await CallbackQuery.message.reply_photo(
                    photo=thumb,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=(
                        f"<b>__چاتی دەنگی لێدا__</b>\n\n🎥<b>__دەستیکرد بەژەنینی مۆسیقا:__ </b>[{title[:25]}](https://www.youtube.com/watch?v={videoid}) \n⏳<b>__ماوە:__</b> {duration_min} \n👤**__داواکراوە لەلایەن:__** {mention}"
                    ),
                )
                os.remove(thumb)

            else:
                await CallbackQuery.message.delete()
                await CallbackQuery.answer("Skipped!", show_alert=True)
                await hama.pytgcalls.change_stream(
                    chat_id,
                    InputStream(
                        InputAudioStream(
                            videoid,
                        ),
                    ),
                )
                afk = videoid
                title = db_mem[videoid]["title"]
                duration_min = db_mem[videoid]["duration"]
                duration_sec = int(time_to_seconds(duration_min))
                mention = db_mem[videoid]["username"]
                videoid = db_mem[videoid]["videoid"]
                if str(videoid) == "smex1":
                    buttons = buttons = audio_markup(
                        videoid,
                        CallbackQuery.from_user.id,
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
                        CallbackQuery.from_user.id,
                        duration_min,
                        duration_min,
                    )
                final_output = await CallbackQuery.message.reply_photo(
                    photo=thumb,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"<b>__چاتی دەنگی لێدا__</b>\n\n🎥<b>__دەستیکرد بەژەنینی مۆسیقا:__</b> {title} \n⏳<b>__ماوە:__</b> {duration_min} \n👤<b>__داواکراوە لەلایەن:__ </b> {mention}",
                )
            await start_timer(
                videoid,
                duration_min,
                duration_sec,
                final_output,
                CallbackQuery.message.chat.id,
                CallbackQuery.message.from_user.id,
                aud,
            )


@app.on_callback_query(filters.regex("audio_video_download"))
async def down_playlisyts(_, CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    videoid, user_id = callback_request.split("|")
    buttons = download_markup(videoid, user_id)
    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"good"))
async def good(_, CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    videoid, user_id = callback_request.split("|")
    buttons = download_markup(videoid, user_id)
    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )
