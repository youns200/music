import asyncio
import os
import random
from asyncio import QueueEmpty

from config import get_queue
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputAudioStream, InputStream

from hama import BOT_USERNAME, MUSIC_BOT_NAME, app, db_mem
from hama.Core.PyTgCalls import Queues, hama
from hama.Core.PyTgCalls.Converter import convert
from hama.Core.PyTgCalls.Downloader import download
from hama.Database import (_get_playlists, delete_playlist, get_playlist,
                            get_playlist_names, is_active_chat, save_playlist)
from hama.Database.queue import (add_active_chat, is_active_chat,
                                  is_music_playing, music_off, music_on,
                                  remove_active_chat)
from hama.Decorators.admins import AdminRightsCheckCB
from hama.Decorators.checker import checkerCB
from hama.Inline import (audio_markup, audio_markup2, download_markup,
                          fetch_playlist, paste_queue_markup, primary_markup)
from hama.Utilities.changers import time_to_seconds
from hama.Utilities.chat import specialfont_to_normal
from hama.Utilities.paste import isPreviewUp, paste_queue
from hama.Utilities.theme import check_theme
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
    filters.regex(pattern=r"^(pausecb|skipcb|stopcb|resumecb)$")
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
    if command == "stopcb":
        try:
            Queues.clear(chat_id)
        except QueueEmpty:
            pass
        await remove_active_chat(chat_id)
        await hama.pytgcalls.leave_group_call(chat_id)
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
                    "Skipped! Playlist Playing....", show_alert=True
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
                theme = await check_theme(chat_id)
                chat_title = await specialfont_to_normal(
                    CallbackQuery.message.chat.title
                )
                thumb = await gen_thumb(
                    thumbnail,
                    title,
                    CallbackQuery.from_user.id,
                    theme,
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


@app.on_callback_query(filters.regex("play_playlist"))
async def play_playlist(_, CallbackQuery):
    global get_queue
    loop = asyncio.get_event_loop()
    callback_data = CallbackQuery.data.strip()
    chat_id = CallbackQuery.message.chat.id
    callback_request = callback_data.split(None, 1)[1]
    user_id, smex, type = callback_request.split("|")
    chat_title = CallbackQuery.message.chat.title
    user_id = int(user_id)
    if chat_id not in db_mem:
        db_mem[chat_id] = {}
    if smex == "third":
        _playlist = await get_playlist_names(user_id, type)
        try:
            user = await app.get_users(user_id)
            third_name = user.first_name
        except:
            third_name = "Deleted Account"
    elif smex == "Personal":
        if CallbackQuery.from_user.id != int(user_id):
            return await CallbackQuery.answer(
                "ئەمە بۆ تۆ نیە! پەخشکردنی لیستی پەخشکردنی خۆت", show_alert=True
            )
        _playlist = await get_playlist_names(user_id, type)
        third_name = CallbackQuery.from_user.first_name
    elif smex == "Group":
        _playlist = await get_playlist_names(
            CallbackQuery.message.chat.id, type
        )
        user_id = CallbackQuery.message.chat.id
        third_name = chat_title
    else:
        return await CallbackQuery.answer("هەڵە لە لیستی پەخشکردن.")
    if not _playlist:
        return await CallbackQuery.answer(
            f"ئەم بەکارهێنەرە هیچ لیستێکی پەخشکردنی نیە لەسەر سێرڤەرەکان.", show_alert=True
        )
    else:
        await CallbackQuery.message.delete()
        mystic = await CallbackQuery.message.reply_text(
            f"دەستکردن بە لیستی پەخشکردن لە {third_name}.\n\nداواکراوە لەلایەن:- {CallbackQuery.from_user.first_name}"
        )
        msg = f"Queued Playlist:\n\n"
        j = 0
        for_t = 0
        for_p = 0
        for shikhar in _playlist:
            _note = await get_playlist(user_id, shikhar, type)
            title = _note["title"]
            videoid = _note["videoid"]
            url = f"https://www.youtube.com/watch?v={videoid}"
            duration = _note["duration"]
            if await is_active_chat(chat_id):
                position = await Queues.put(chat_id, file=videoid)
                j += 1
                for_p = 1
                msg += f"{j}- {title[:50]}\n"
                msg += f"Queued Position- {position}\n\n"
                if videoid not in db_mem:
                    db_mem[videoid] = {}
                db_mem[videoid]["username"] = CallbackQuery.from_user.mention
                db_mem[videoid]["chat_title"] = chat_title
                db_mem[videoid]["user_id"] = user_id
                got_queue = get_queue.get(CallbackQuery.message.chat.id)
                title = title
                user = CallbackQuery.from_user.first_name
                duration = duration
                to_append = [title, user, duration]
                got_queue.append(to_append)
            else:
                loop = asyncio.get_event_loop()
                send_video = videoid
                for_t = 1
                (
                    title,
                    duration_min,
                    duration_sec,
                    thumbnail,
                ) = get_yt_info_id(videoid)
                mystic = await mystic.edit(
                    f"**{MUSIC_BOT_NAME} داگرتن**\n\n**ناونیشان:** {title[:50]}\n\n0% ▓▓▓▓▓▓▓▓▓▓▓▓ 100%"
                )
                downloaded_file = await loop.run_in_executor(
                    None, download, videoid, mystic, title
                )
                raw_path = await convert(downloaded_file)
                try:
                    await hama.pytgcalls.join_group_call(
                        chat_id,
                        InputStream(
                            InputAudioStream(
                                raw_path,
                            ),
                        ),
                        stream_type=StreamType().local_stream,
                    )
                except Exception as e:
                    return await mystic.edit(
                        "هەڵە لە چوونە پاڵ دەنگی چات. دڵنیابە لەوەی کە چات دەنگی چالاک کراوە."
                    )
                theme = await check_theme(chat_id)
                chat_title = await specialfont_to_normal(chat_title)
                thumb = await gen_thumb(
                    thumbnail,
                    title,
                    CallbackQuery.from_user.id,
                    theme,
                    chat_title,
                )
                buttons = primary_markup(
                    videoid,
                    CallbackQuery.from_user.id,
                    duration_min,
                    duration_min,
                )
                await mystic.delete()
                get_queue[CallbackQuery.message.chat.id] = []
                got_queue = get_queue.get(CallbackQuery.message.chat.id)
                title = title
                user = CallbackQuery.from_user.first_name
                duration = duration_min
                to_append = [title, user, duration]
                got_queue.append(to_append)
                await music_on(chat_id)
                await add_active_chat(chat_id)
                cap = f"🎥<b>__گۆرانی ژەنین:__ </b>[{title[:25]}](https://www.youtube.com/watch?v={videoid}) \n💡<b>__زانیاری:__</b> [زانیاری زیاتر بهێنە](https://t.me/{BOT_USERNAME}?start=info_{videoid})\n👤**__داواکراوە لەلایەن:__** {CallbackQuery.from_user.mention}"
                final_output = await CallbackQuery.message.reply_photo(
                    photo=thumb,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=cap,
                )
                os.remove(thumb)
        await mystic.delete()
        if for_p == 1:
            m = await CallbackQuery.message.reply_text(
                "لکاندنی لیستی پەخشکردنی ڕیزکراو بۆ بین"
            )
            link = await paste_queue(msg)
            preview = link + "/preview.png"
            url = link + "/index.txt"
            buttons = paste_queue_markup(url)
            if await isPreviewUp(preview):
                await CallbackQuery.message.reply_photo(
                    photo=preview,
                    caption=f"ئەمە لیستی پەخشکردنی ڕیزکراوە لە {third_name}.\n\nپەخشکراوە لەلایەن :- {CallbackQuery.from_user.mention}",
                    quote=False,
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
                await m.delete()
            else:
                await CallbackQuery.message.reply_text(
                    text=msg, reply_markup=audio_markup2
                )
                await m.delete()
        else:
            await CallbackQuery.message.reply_text(
                "تەنها 1 مووزیک لە لیستی پەخش کردن. چیتر مووزیک بۆ زیادکردن لە ڕیزدا نیە."
            )
        if for_t == 1:
            await start_timer(
                send_video,
                duration_min,
                duration_sec,
                final_output,
                CallbackQuery.message.chat.id,
                CallbackQuery.message.from_user.id,
                0,
            )


@app.on_callback_query(filters.regex("add_playlist"))
async def group_playlist(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, type, genre = callback_request.split("|")
    if type == "Personal":
        user_id = CallbackQuery.from_user.id
    elif type == "Group":
        a = await app.get_chat_member(
            CallbackQuery.message.chat.id, CallbackQuery.from_user.id
        )
        if not a.can_manage_voice_chats:
            return await CallbackQuery.answer(
                "تۆ مۆڵەتی پێویستت نیە بۆ ئەنجامدانی ئەم کردارە. مۆڵەت: بەڕێوەبردنی دەنگ چاتەکان",
                show_alert=True,
            )
        user_id = CallbackQuery.message.chat.id
    _count = await get_playlist_names(user_id, genre)
    if not _count:
        sex = await CallbackQuery.message.reply_text(
            f"بەخێربێیت بۆ {MUSIC_BOT_NAME} تایبەتمەندی لیستی پەخشکردن.\n\nدروستکردنی لیستی پەخشکردنەکەت لە بنکەی زانیاریدا تکایه چاوەڕوان بکه.\n\n:- {genre}"
        )
        await asyncio.sleep(2)
        await sex.delete()
        count = len(_count)
    else:
        count = len(_count)
    count = int(count)
    if count == 50:
        return await CallbackQuery.answer(
            "ببووره! تۆ تەنها دەتوانیت 50 مۆسیقات هەبێت لە لیستی پەخشکردن.",
            show_alert=True,
        )
    loop = asyncio.get_event_loop()
    await CallbackQuery.answer()
    title, duration_min, duration_sec, thumbnail = get_yt_info_id(videoid)
    _check = await get_playlist(user_id, videoid, genre)
    title = title[:50]
    if _check:
        return await CallbackQuery.message.reply_text(
            f"{CallbackQuery.from_user.mention}, پێشتر لە لیستی پەخشکردندایە!"
        )
    assis = {
        "videoid": videoid,
        "title": title,
        "duration": duration_min,
    }
    await save_playlist(user_id, videoid, assis, genre)
    Name = CallbackQuery.from_user.first_name
    return await CallbackQuery.message.reply_text(
        f"زیادکرا بۆ لیستی پەخشکردن لەلایەن {CallbackQuery.from_user.mention}"
    )


@app.on_callback_query(filters.regex("check_playlist"))
async def check_playlist(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    type, genre = callback_request.split("|")
    if type == "Personal":
        user_id = CallbackQuery.from_user.id
        user_name = CallbackQuery.from_user.first_name
    elif type == "Group":
        user_id = CallbackQuery.message.chat.id
        user_name = CallbackQuery.message.chat.title
    _playlist = await get_playlist_names(user_id, genre)
    if not _playlist:
        return await CallbackQuery.answer(
            f" لیستی پەخش کردن لەسەر سێرڤەرەکان. هەوڵ بدە مۆسیقا زیادبکە لە لیستی پەخشکردن.",
            show_alert=True,
        )
    else:
        j = 0
        await CallbackQuery.answer()
        await CallbackQuery.message.delete()
        msg = f"لیستی پەخشی هەڵچنراو:\n\n"
        for shikhar in _playlist:
            j += 1
            _note = await get_playlist(user_id, shikhar, genre)
            title = _note["title"]
            duration = _note["duration"]
            msg += f"{j}- {title[:60]}\n"
            msg += f"    ماوە- {duration}\n\n"
        m = await CallbackQuery.message.reply_text("لکاندنی لیستی پەخشکردن بۆ بین")
        link = await paste_queue(msg)
        preview = link + "/preview.png"
        url = link + "/index.txt"
        buttons = fetch_playlist(
            user_name, type, genre, CallbackQuery.from_user.id, url
        )
        if await isPreviewUp(preview):
            await CallbackQuery.message.reply_photo(
                photo=preview,
                caption=f"ئەمە لیستی پەخشکردنە لە {user_name}.",
                quote=False,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            await m.delete()
        else:
            await CallbackQuery.message.reply_text(
                text=msg, reply_markup=audio_markup2
            )
            await m.delete()


@app.on_callback_query(filters.regex("delete_playlist"))
async def del_playlist(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    type, genre = callback_request.split("|")
    if str(type) == "Personal":
        user_id = CallbackQuery.from_user.id
        user_name = CallbackQuery.from_user.first_name
    elif str(type) == "Group":
        a = await app.get_chat_member(
            CallbackQuery.message.chat.id, CallbackQuery.from_user.id
        )
        if not a.can_manage_voice_chats:
            return await CallbackQuery.answer(
                "تۆ مۆڵەتی پێویستت نیە بۆ ئەنجامدانی ئەم کردارە. مۆڵەت: بەڕێوەبردنی دەنگ چاتەکان",
                show_alert=True,
            )
        user_id = CallbackQuery.message.chat.id
        user_name = CallbackQuery.message.chat.title
    _playlist = await get_playlist_names(user_id, genre)
    if not _playlist:
        return await CallbackQuery.answer(
            "گروپ هیچ لیستێکی پەخشکردنی نیە لەسەر سێرڤەری بۆت", show_alert=True
        )
    else:
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()
        for shikhar in _playlist:
            await delete_playlist(user_id, shikhar, genre)
    await CallbackQuery.message.reply_text(
        f"Successfully deleted {type}'s {genre} whole playlist\n\nBy :- {CallbackQuery.from_user.mention}"
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
