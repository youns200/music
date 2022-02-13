import asyncio
import os
import shutil
import subprocess
from sys import version as pyver

from config import get_queue
from pyrogram import Client, filters
from pyrogram.types import Message

from hama import SUDOERS, app, db_mem, userbot
from hama.Database import get_active_chats, is_active_chat
from hama.Decorators.checker import checker, checkerCB
from hama.Inline import primary_markup

from pyrogram.types import (InlineKeyboardMarkup, InputMediaPhoto, Message,
                            Voice)

loop = asyncio.get_event_loop()

__MODULE__ = "Join/Leave"
__HELP__ = """

**Note:**
Only for Sudo Users


/joinassistant [Chat Username or Chat ID]
- Join assistant to a group.

/leaveassistant [Chat Username or Chat ID]
- Assistant will leave the particular group.

/leavebot [Chat Username or Chat ID]
- Bot will leave the particular chat.

"""



@app.on_callback_query(filters.regex("pr_go_back_timer"))
async def pr_go_back_timer(_, CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, user_id = callback_request.split("|")
    if await is_active_chat(CallbackQuery.message.chat.id):
        if db_mem[CallbackQuery.message.chat.id]["videoid"] == videoid:
            dur_left = db_mem[CallbackQuery.message.chat.id]["left"]
            duration_min = db_mem[CallbackQuery.message.chat.id]["total"]
            buttons = primary_markup(videoid, user_id, dur_left, duration_min)
            await CallbackQuery.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
             
    
    

@app.on_callback_query(filters.regex("timer_checkup_markup"))
async def timer_checkup_markup(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, user_id = callback_request.split("|")
    if await is_active_chat(CallbackQuery.message.chat.id):
        if db_mem[CallbackQuery.message.chat.id]["videoid"] == videoid:
            dur_left = db_mem[CallbackQuery.message.chat.id]["left"]
            duration_min = db_mem[CallbackQuery.message.chat.id]["total"]
            return await CallbackQuery.answer(
                f"ماوە {dur_left} لە {duration_min} خولەک.",
                show_alert=True,
            )
        return await CallbackQuery.answer(f"پەخش نەکراوە.", show_alert=True)
    else:
        return await CallbackQuery.answer(
            f"چاتی دەنگی چاڵاک نیە", show_alert=True
        )


@app.on_message(filters.command("queue"))
async def activevc(_, message: Message):
    global get_queue
    if await is_active_chat(message.chat.id):
        mystic = await message.reply_text("Please Wait... Getting Queue..")
        dur_left = db_mem[message.chat.id]["left"]
        duration_min = db_mem[message.chat.id]["total"]
        got_queue = get_queue.get(message.chat.id)
        if not got_queue:
            await mystic.edit(f"Nothing in Queue")
        fetched = []
        for get in got_queue:
            fetched.append(get)

        ### Results
        current_playing = fetched[0][0]
        user_name = fetched[0][1]

        msg = "**لیستی ڕێز**\n\n"
        msg += "**لە ئێستادا پەخش دەکات:**"
        msg += "\n▶️" + current_playing[:30]
        msg += f"\n   ╚لەلایەن:- {user_name}"
        msg += f"\n   ╚کات:- ماوە `{dur_left}` لە دەرەوە `{duration_min}` خوڵەک."
        fetched.pop(0)
        if fetched:
            msg += "\n\n"
            msg += "**سەرەوەی داهاتوو لە ڕیز:**"
            for song in fetched:
                name = song[0][:30]
                usr = song[1]
                dur = song[2]
                msg += f"\n⏸️{name}"
                msg += f"\n   ╠کات : {dur}"
                msg += f"\n   ╚داواکراوە لەلایەن : {usr}\n"
        if len(msg) > 4096:
            await mystic.delete()
            filename = "queue.txt"
            with open(filename, "w+", encoding="utf8") as out_file:
                out_file.write(str(msg.strip()))
            await message.reply_document(
                document=filename,
                caption=f"**دەرچوون:**\n\n`لیستی ڕێز`",
                quote=False,
            )
            os.remove(filename)
        else:
            await mystic.edit(msg)
    else:
        await message.reply_text(f"هیچ شتێک لە ڕیزدا نیە")


@app.on_message(filters.command("activevc") & filters.user(SUDOERS))
async def activevc(_, message: Message):
    served_chats = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        await message.reply_text(f"**هەڵەڕوویدا:-** {e}")
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
        except Exception:
            title = "Private Group"
        if (await app.get_chat(x)).username:
            user = (await app.get_chat(x)).username
            text += (
                f"<b>{j + 1}.</b>  [{title}](https://t.me/{user})[`{x}`]\n"
            )
        else:
            text += f"<b>{j + 1}. {title}</b> [`{x}`]\n"
        j += 1
    if not text:
        await message.reply_text("چاتی دەنگی چاڵاکرنەکراوە")
    else:
        await message.reply_text(
            f"**چاتی دەنگی چاڵاکرا:-**\n\n{text}",
            disable_web_page_preview=True,
        )


@app.on_message(filters.command("join") & filters.user(SUDOERS))
async def basffy(_, message):
    if len(message.command) != 2:
        await message.reply_text(
            "**بەکاربێنە:**\n/joinassistant [پێناسە یان ناسنامەی گروپ]"
        )
        return
    chat = message.text.split(None, 2)[1]
    try:
        await userbot.join_chat(chat)
    except Exception as e:
        await message.reply_text(f"سەرکەوتونەبوو\n**هۆکار**:{e}")
        return
    await message.reply_text("داخڵ بو.")


@app.on_message(filters.command("leavebot") & filters.user(SUDOERS))
async def baaaf(_, message):
    if len(message.command) != 2:
        await message.reply_text(
            "**بەکارهێنەر:**\n/leavebot [پێناسە یان ناسنامەی گروپ]"
        )
        return
    chat = message.text.split(None, 2)[1]
    try:
        await app.leave_chat(chat)
    except Exception as e:
        await message.reply_text(f"سەرکەوتونەبو\n**هۆکار**:{e}")
        print(e)
        return
    await message.reply_text("دەرچۆ بۆت")


@app.on_message(filters.command("leave") & filters.user(SUDOERS))
async def baujaf(_, message):
    if len(message.command) != 2:
        await message.reply_text(
            "**بەبەکارهێنانی:**\n/leave [ناسمە یان پێناسەی گروپ]"
        )
        return
    chat = message.text.split(None, 2)[1]
    try:
        await userbot.leave_chat(chat)
    except Exception as e:
        await message.reply_text(f"سەرکەوتونەبو\n**هۆکار**:{e}")
        return
    await message.reply_text("دەرچۆ.")

@app.on_message(filters.command("leaveall") & filters.user(SUDOERS))
async def leave_all(client, message):
    if message.from_user.id not in SUDOERS:
        return

    left = 0
    failed = 0
    
    msg = await message.reply("🔄 یارمەتی دەر لەگروپەکان دەرەچێ!")
    async for dialog in user.iter_dialogs():
        try:
            await user.leave_chat(dialog.chat.id)
            await remove_active_chat(dialog.chat.id)
            left += 1
            await msg.edit(
                f"یوسەر بۆت لەگروپەکان دەرەچێ...\n\nدەرچۆن: {left} لە گروپ.\nسەرکەوتونەبوو: {failed} ."
            )
        except BaseException:
            failed += 1
            await msg.edit(
                f"یارمەتی دەر لەگروپەکان دەرەچێ وا...\n\nدەرچۆ لە: {left} گرووپ.\nسەرکەوتونەبوو: {failed} ."
            )
        await asyncio.sleep(0.7)
    await msg.delete()
    await Client.send_message(
        message.chat.id, f"✅ دەرچوەکان: {left} .\n❌ سەرکەوتو نەبوو لە: {failed} گروپ."
    )


@app.on_message(filters.left_chat_member)
async def bot_kicked(c: Client, m: Message):
    bot_id = (await c.get_me()).id
    chat_id = m.chat.id
    left_member = m.left_chat_member
    if left_member.id == bot_id:
        await user.leave_chat(chat_id)
        await remove_served_chat(chat_id)
        await remove_active_chat(chat_id)
