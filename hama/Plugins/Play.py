import asyncio
from os import path

from pyrogram import filters
from pyrogram.types import (InlineKeyboardMarkup, InputMediaPhoto, Message,
                            Voice)
from youtube_search import YoutubeSearch

from hama import (BOT_USERNAME, DURATION_LIMIT, DURATION_LIMIT_MIN,
                   MUSIC_BOT_NAME, app, db_mem)
from hama.Core.PyTgCalls.Converter import convert
from hama.Core.PyTgCalls.Downloader import download
from hama.Decorators.assistant import AssistantAdd
from hama.Decorators.checker import checker
from hama.Decorators.permission import PermissionCheck
from hama.Inline import (search_markup, search_markup2,
                          url_markup, url_markup2)
from hama.Utilities.changers import seconds_to_min, time_to_seconds
from hama.Utilities.chat import specialfont_to_normal
from hama.Utilities.stream import start_stream, start_stream_audio
from hama.Utilities.theme import check_theme
from hama.Utilities.thumbnails import gen_thumb
from hama.Utilities.url import get_url
from hama.Utilities.youtube import (get_yt_info_id, get_yt_info_query,
                                     get_yt_info_query_slider)

loop = asyncio.get_event_loop()


@app.on_message(
    filters.command(["play", f"play@{BOT_USERNAME}"]) & filters.group
)
@checker
@PermissionCheck
@AssistantAdd
async def play(_, message: Message):
    await message.delete()
    if message.chat.id not in db_mem:
        db_mem[message.chat.id] = {}
    if message.sender_chat:
        return await message.reply_text(
            "تۆ __Anonymous Admin__ لەم گروپەی چات! گەڕانەوە بۆ ئەژمێری بەکارهێنەر لە مافەکانی بەڕێوەبەر."
        )
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)
    if audio:
        mystic = await message.reply_text(
            "🔍"
        )

        if audio.file_size > 157286400:
            return await mystic.edit_text(
                "قەبارەی فایلی دەنگ پێویستە کەمتر بێت لە 150 مێگابایت"
            )
        duration_min = seconds_to_min(audio.duration)
        duration_sec = audio.duration
        if (audio.duration) > DURATION_LIMIT:
            return await mystic.edit_text(
                f"**سنووری ماوە تێپەڕێنراوە**\n\n**سنووری ماوە تێپەڕێنراوە ...: **{DURATION_LIMIT_MIN} \n**ماوەی ڕێپێدراو ...:** {duration_min} "
            )
        file_name = (
            audio.file_unique_id
            + "."
            + (
                (audio.file_name.split(".")[-1])
                if (not isinstance(audio, Voice))
                else "ogg"
            )
        )
        file_name = path.join(path.realpath("downloads"), file_name)
        file = await convert(
            (await message.reply_to_message.download(file_name))
            if (not path.isfile(file_name))
            else file_name,
        )
        return await start_stream_audio(
            message,
            file,
            "smex1",
            "Given Audio Via Telegram",
            duration_min,
            duration_sec,
            mystic,
        )
    elif url:
        mystic = await message.reply_text("🔍")
        query = message.text.split(None, 1)[1]
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
        ) = get_yt_info_query(query)
        await mystic.delete()
        buttons = url_markup2(videoid, duration_min, message.from_user.id)
        return await message.reply_photo(
            photo=thumb,
            caption=f"📎ناونیشان: **{title}\n\n⏳ماوە:** {duration_min}\n\n__[زانیاری زیاتر بهێنە دەربارەی ڤیدیۆ](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        mystic = await message.reply_text("🔍")
        query = message.text.split(None, 1)[1]
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
        ) = get_yt_info_query(query)
        await mystic.delete()
        buttons = url_markup(
            videoid, duration_min, message.from_user.id, query, 0
        )
        return await message.reply_photo(
            photo=thumb,
            caption=f"📎ناونیشان: **{title}\n\n⏳ماوە:** {duration_min}\n\n__[زانیاری زیاتر بهێنە دەربارەی ڤیدیۆ](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@app.on_callback_query(filters.regex(pattern=r"hama"))
async def startyuplay(_, CallbackQuery):
    if CallbackQuery.message.chat.id not in db_mem:
        db_mem[CallbackQuery.message.chat.id] = {}
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    chat_id = CallbackQuery.message.chat.id
    chat_title = CallbackQuery.message.chat.title
    videoid, duration, user_id = callback_request.split("|")
    if str(duration) == "None":
        return await CallbackQuery.answer(
            f"ببووره! ڤیدیۆیەکی ڕاستەوخۆیە.", show_alert=True
        )
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "گەران بۆ گۆرانیەک بکە ، چونکە ئەمە بۆتۆ ڕێگە پێدراو نیە.", show_alert=True
        )
    await CallbackQuery.message.delete()
    title, duration_min, duration_sec, thumbnail = get_yt_info_id(videoid)
    if duration_sec > DURATION_LIMIT:
        return await CallbackQuery.message.reply_text(
            f"**۰ ماوەی درێژکراوەی سنوور: {DURATION_LIMIT_MIN} ماوەی دیاریکراوی خولەک: {duration_min} خولەک"
        )
    await CallbackQuery.answer(f"پڕۆسە:- {title[:20]}", show_alert=True)
    mystic = await CallbackQuery.message.reply_text(
        f"🔍 :- {title[:50]}"
    )
    downloaded_file = await loop.run_in_executor(
        None, download, videoid, mystic, title
    )
    raw_path = await convert(downloaded_file)
    theme = await check_theme(chat_id)
    chat_title = await specialfont_to_normal(chat_title)
    thumb = await gen_thumb(thumbnail, title, user_id, theme, chat_title)
    if chat_id not in db_mem:
        db_mem[chat_id] = {}
    await start_stream(
        CallbackQuery,
        raw_path,
        videoid,
        thumb,
        title,
        duration_min,
        duration_sec,
        mystic,
    )


@app.on_callback_query(filters.regex(pattern=r"Search"))
async def search_query_more(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    query, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "گەران بۆ گۆرانیەک بکە ، چونکە ئەمە بۆتۆ ڕێگە پێدراو نیە.",
            show_alert=True,
        )
    await CallbackQuery.answer("گەڕان بۆ بەدەست هێنانی ئەنجامی زیاتر")
    results = YoutubeSearch(query, max_results=5).to_dict()
    med = InputMediaPhoto(
        media="Utils/1(10).jpg",
        caption=(
            f"1️⃣<b>{results[0]['title']}</b>\n  ┗  🔗 <u>__[دەستکەوتنی زانیاری زیاتری ڤیدیۆ ](https://t.me/{BOT_USERNAME}?start=info_{results[0]['id']})__</u>\n\n2️⃣<b>{results[1]['title']}</b>\n  ┗  🔗 <u>__[دەستکەوتنی زانیاری زیاتری ڤیدیۆ ](https://t.me/{BOT_USERNAME}?start=info_{results[1]['id']})__</u>\n\n3️⃣<b>{results[2]['title']}</b>\n  ┗  🔗 <u>__[دەستکەوتنی زانیاری زیاتری ڤیدیۆ ](https://t.me/{BOT_USERNAME}?start=info_{results[2]['id']})__</u>\n\n4️⃣<b>{results[3]['title']}</b>\n  ┗  🔗 <u>__[دەستکەوتنی زانیاری زیاتری ڤیدیۆ ](https://t.me/{BOT_USERNAME}?start=info_{results[3]['id']})__</u>\n\n5️⃣<b>{results[4]['title']}</b>\n  ┗  🔗 <u>__[دەستکەوتنی زانیاری زیاتری ڤیدیۆ ](https://t.me/{BOT_USERNAME}?start=info_{results[4]['id']})__</u>"
        ),
    )
    buttons = search_markup(
        results[0]["id"],
        results[1]["id"],
        results[2]["id"],
        results[3]["id"],
        results[4]["id"],
        results[0]["duration"],
        results[1]["duration"],
        results[2]["duration"],
        results[3]["duration"],
        results[4]["duration"],
        user_id,
        query,
    )
    return await CallbackQuery.edit_message_media(
        media=med, reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"popat"))
async def popat(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    i, query, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "گەران بۆ گۆرانیەک بکە ، چونکە ئەمە بۆتۆ ڕێگە پێدراو نیە", show_alert=True
        )
    results = YoutubeSearch(query, max_results=10).to_dict()
    if int(i) == 1:
        buttons = search_markup2(
            results[5]["id"],
            results[6]["id"],
            results[7]["id"],
            results[8]["id"],
            results[9]["id"],
            results[5]["duration"],
            results[6]["duration"],
            results[7]["duration"],
            results[8]["duration"],
            results[9]["duration"],
            user_id,
            query,
        )
        await CallbackQuery.edit_message_text(
            f"6️⃣<b>{results[5]['title']}</b>\n  ┗  🔗 <u>__[دەستکەوتنی زانیاری زیاتری ڤیدیۆ ](https://t.me/{BOT_USERNAME}?start=info_{results[5]['id']})__</u>\n\n7️⃣<b>{results[6]['title']}</b>\n  ┗  🔗 <u>__[دەستکەوتنی زانیاری زیاتری ڤیدیۆ ](https://t.me/{BOT_USERNAME}?start=info_{results[6]['id']})__</u>\n\n8️⃣<b>{results[7]['title']}</b>\n  ┗  🔗 <u>__[دەستکەوتنی زانیاری زیاتری ڤیدیۆ ](https://t.me/{BOT_USERNAME}?start=info_{results[7]['id']})__</u>\n\n9️⃣<b>{results[8]['title']}</b>\n  ┗  🔗 <u>__[دەستکەوتنی زانیاری زیاتری ڤیدیۆ ](https://t.me/{BOT_USERNAME}?start=info_{results[8]['id']})__</u>\n\n🔟<b>{results[9]['title']}</b>\n  ┗  🔗 <u>__[دەستکەوتنی زانیاری زیاتری ڤیدیۆ ](https://t.me/{BOT_USERNAME}?start=info_{results[9]['id']})__</u>",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        disable_web_page_preview = True
        return
    if int(i) == 2:
        buttons = search_markup(
            results[0]["id"],
            results[1]["id"],
            results[2]["id"],
            results[3]["id"],
            results[4]["id"],
            results[0]["duration"],
            results[1]["duration"],
            results[2]["duration"],
            results[3]["duration"],
            results[4]["duration"],
            user_id,
            query,
        )
        await CallbackQuery.edit_message_text(
            f"1️⃣<b>{results[0]['title']}</b>\n  ┗  🔗 <u>__[دەستکەوتنی زانیاری زیاتری ڤیدیۆ ](https://t.me/{BOT_USERNAME}?start=info_{results[0]['id']})__</u>\n\n2️⃣<b>{results[1]['title']}</b>\n  ┗  🔗 <u>__[دەستکەوتنی زانیاری زیاتری ڤیدیۆ ](https://t.me/{BOT_USERNAME}?start=info_{results[1]['id']})__</u>\n\n3️⃣<b>{results[2]['title']}</b>\n  ┗  🔗 <u>__[دەستکەوتنی زانیاری زیاتری ڤیدیۆ ](https://t.me/{BOT_USERNAME}?start=info_{results[2]['id']})__</u>\n\n4️⃣<b>{results[3]['title']}</b>\n  ┗  🔗 <u>__[دەستکەوتنی زانیاری زیاتری ڤیدیۆ ](https://t.me/{BOT_USERNAME}?start=info_{results[3]['id']})__</u>\n\n5️⃣<b>{results[4]['title']}</b>\n  ┗  🔗 <u>__[دەستکەوتنی زانیاری زیاتری ڤیدیۆ ](https://t.me/{BOT_USERNAME}?start=info_{results[4]['id']})__</u>",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        disable_web_page_preview = True
        return


@app.on_callback_query(filters.regex(pattern=r"slider"))
async def slider_query_results(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    what, type, query, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer(
            "گەران بۆ گۆرانیەک بکە ، چونکە ئەمە بۆتۆ ڕێگە پێدراو نیە.",
            show_alert=True,
        )
    what = str(what)
    type = int(type)
    if what == "F":
        if type == 9:
            query_type = 0
        else:
            query_type = int(type + 1)
        await CallbackQuery.answer("بەدەست هێنانی ئەنجامی داهاتو", show_alert=True)
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
        ) = get_yt_info_query_slider(query, query_type)
        buttons = url_markup(
            videoid, duration_min, user_id, query, query_type
        )
        med = InputMediaPhoto(
            media=thumb,
            caption=f"📎ناو: **{title}\n\n⏳کات:** {duration_min} خوڵەک\n\n__[بۆ بینینی زانیاری لەسەر ڤیدیۆ](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
        )
        return await CallbackQuery.edit_message_media(
            media=med, reply_markup=InlineKeyboardMarkup(buttons)
        )
    if what == "B":
        if type == 0:
            query_type = 9
        else:
            query_type = int(type - 1)
        await CallbackQuery.answer("بەدەستهێنانی ئەنجامی پێشوو", show_alert=True)
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
        ) = get_yt_info_query_slider(query, query_type)
        buttons = url_markup(
            videoid, duration_min, user_id, query, query_type
        )
        med = InputMediaPhoto(
            media=thumb,
            caption=f"📎ناو: **{title}\n\n⏳کات:** {duration_min} خولەک\n\n__[بۆ بینینی زانیاری لەسەر ڤیدیۆ](https://t.me/{BOT_USERNAME}?start=info_{videoid})__",
        )
        return await CallbackQuery.edit_message_media(
            media=med, reply_markup=InlineKeyboardMarkup(buttons)
        )
