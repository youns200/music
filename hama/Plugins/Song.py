import asyncio
from os import path

from pyrogram import filters
from pyrogram.types import (InlineKeyboardMarkup, InputMediaPhoto, Message,
                            Voice)
from youtube_search import YoutubeSearch

from hama import (BOT_USERNAME, DURATION_LIMIT, DURATION_LIMIT_MIN,
                   MUSIC_BOT_NAME, app, db_mem)
from hama.Decorators.permission import PermissionCheck
from hama.Inline import song_download_markup, song_markup
from hama.Utilities.url import get_url
from hama.Utilities.youtube import (get_yt_info_query,
                                     get_yt_info_query_slider)

loop = asyncio.get_event_loop()

__MODULE__ = "داگرتنی گۆرانی"
__HELP__ = """


/song [لینکی یوتوب ] 
- بۆ دابەزاندنی ڤیدیۆ و گۆرانی.



"""


@app.on_message(
    filters.command(["song", f"song@{BOT_USERNAME}"]) & filters.group
)
@PermissionCheck
async def play(_, message: Message):
    if message.sender_chat:
        return await message.reply_text(
            "تۆ __Anonymous Admin__ لەم گروپی چاتەدا!\nهەوڵبدە خۆت بگەڕێینەوە بۆ بەڕێوەبەری ئاسایی."
        )
    await message.delete()
    url = get_url(message)
    if url:
        mystic = await message.reply_text("🔄 پرۆسەی لینک... تکایە چاوەڕوان بە!")
        query = message.text.split(None, 1)[1]
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
        ) = await loop.run_in_executor(None, get_yt_info_query, query)
        if str(duration_min) == "None":
            return await mystic.edit("ببوورە ئەم ڤیدیۆیە ڕاستەوخۆیە")
        await mystic.delete()
        buttons = song_download_markup(videoid, message.from_user.id)
        return await message.reply_photo(
            photo=thumb,
            caption=f"📎ناو: **{title}\n\n⏳کات:** {duration_min} خوڵەک\n\n__[ئێرە دابگرە بۆ بینینی زانیاری ڤیدیۆ](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        if len(message.command) < 2:
            await message.reply_text(
                "**بە فرمانی:**\n\n/song [لینکی یوتوب یان ناوی گۆرانی بنوسە]\n\nبۆ داگرتنی ڤیدیۆ."
            )
            return
        mystic = await message.reply_text("🔍 گەران بۆ دابەزاندن...")
        query = message.text.split(None, 1)[1]
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
        ) = await loop.run_in_executor(None, get_yt_info_query, query)
        if str(duration_min) == "None":
            return await mystic.edit("ببوورە ئەمە ڤیدیۆی ڕاستەوخۆیە")
        await mystic.delete()
        buttons = song_markup(
            videoid, duration_min, message.from_user.id, query, 0
        )
        return await message.reply_photo(
            photo=thumb,
            caption=f"📎ناو: **{title}\n\n⏳کات:** {duration_min} خوڵەک\n\n__[بۆ بینینی زانیاری لەسەر ڤیدیۆ](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@app.on_callback_query(filters.regex("qwertyuiopasdfghjkl"))
async def qwertyuiopasdfghjkl(_, CallbackQuery):
    print("234")
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    videoid, user_id = callback_request.split("|")
    buttons = song_download_markup(videoid, user_id)
    await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"song_right"))
async def song_right(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    what, type, query, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "گەڕان لە مۆسیقای خۆت. ڕێگەت پێنەدراوە ئەم دوگمە بەکاربهێنیت.",
            show_alert=True,
        )
    what = str(what)
    type = int(type)
    if what == "F":
        if type == 9:
            query_type = 0
        else:
            query_type = int(type + 1)
        await CallbackQuery.answer("دەستکەوتنی ئەنجامی داهاتوو", show_alert=True)
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
        ) = await loop.run_in_executor(
            None, get_yt_info_query_slider, query, query_type
        )
        buttons = song_markup(
            videoid, duration_min, user_id, query, query_type
        )
        med = InputMediaPhoto(
            media=thumb,
            caption=f"📎ناو: **{title}\n\n⏳کات:** {duration_min} خوڵەک\n\n__[ـبۆ بینینی زانیاری لەسەر ڤیدیۆ](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
        )
        return await CallbackQuery.edit_message_media(
            media=med, reply_markup=InlineKeyboardMarkup(buttons)
        )
    if what == "B":
        if type == 0:
            query_type = 9
        else:
            query_type = int(type - 1)
        await CallbackQuery.answer("دەستکەوتنی ئەنجامی پێشوو", show_alert=True)
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
        ) = await loop.run_in_executor(
            None, get_yt_info_query_slider, query, query_type
        )
        buttons = song_markup(
            videoid, duration_min, user_id, query, query_type
        )
        med = InputMediaPhoto(
            media=thumb,
            caption=f"📎ناوت: **{title}\n\n⏳کات:** {duration_min} خولەک\n\n__[بینینی زانیاری لەسەر ڤیدیۆ](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
        )
        return await CallbackQuery.edit_message_media(
            media=med, reply_markup=InlineKeyboardMarkup(buttons)
        )
