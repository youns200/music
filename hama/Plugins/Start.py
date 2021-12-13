import asyncio
import time
from sys import version as pyver
from typing import Dict, List, Union

import psutil
from pyrogram import filters
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)

from hama import ASSID, BOT_ID, MUSIC_BOT_NAME, OWNER_ID, SUDOERS, app
from hama import boottime as bot_start_time
from hama import db
from hama.Core.PyTgCalls import hama
from hama.Database import (add_nonadmin_chat, add_served_chat,
                            blacklisted_chats, get_assistant, get_authuser,
                            get_authuser_names, is_nonadmin_chat,
                            is_served_chat, remove_active_chat,
                            remove_nonadmin_chat, save_assistant)
from hama.Decorators.admins import ActualAdminCB
from hama.Decorators.permission import PermissionCheck
from hama.Inline import (custommarkup, dashmarkup, setting_markup, setting_markup2,
                          start_pannel, usermarkup, volmarkup)
from hama.Utilities.ping import get_readable_time

welcome_group = 2

__MODULE__ = "Essentials"
__HELP__ = """


/start 
- Start the Bot.

/help 
- Get Commands Helper Menu.
/settings
- Get Settings DashBoard.
"""


@app.on_message(filters.new_chat_members, group=welcome_group)
async def welcome(_, message: Message):
    chat_id = message.chat.id
    if await is_served_chat(chat_id):
        pass
    else:
        await add_served_chat(chat_id)
    if chat_id in await blacklisted_chats():
        await message.reply_text(
            f"ببوورە, ئەم گروپە[{message.chat.title}] سزادراوە!\n\nپەیوەندی بە بەڕێوەبەری بۆت بکە بۆ یارمەتی"
        )
        await app.leave_chat(chat_id)
    for member in message.new_chat_members:
        try:
            if member.id in OWNER_ID:
                return await message.reply_text(
                    f"{MUSIC_BOT_NAME} داڕێژەری بۆت [{member.mention}] پەیوەندی بەم گروپ چاتە کرد."
                )
            if member.id in SUDOERS:
                return await message.reply_text(
                    f" {MUSIC_BOT_NAME} بەڕێوەبەری بۆت [{member.mention}] پەیوەندی بەم گروپ چاتە کرد."
                )
            if member.id == ASSID:
                await remove_active_chat(chat_id)
            if member.id == BOT_ID:
                out = start_pannel()
                await message.reply_text(
                    f"سلاو من {MUSIC_BOT_NAME}\n\nپێویستە بەرزبکرێمەوە بۆ بەڕێوەبەری گروپ بۆ ئەوەی بتوانم کار بکەم.",
                    reply_markup=InlineKeyboardMarkup(out[1]),
                )
                return
        except:
            return


@app.on_message(filters.command(["help", "start"]) & filters.group)
@PermissionCheck
async def useradd(_, message: Message):
    out = start_pannel()
    await asyncio.gather(
        message.delete(),
        message.reply_text(
            f"سوپاس بۆ گروپی  {message.chat.title}.\n{MUSIC_BOT_NAME} من ئیستا چاڵاکم.\n\n.",
            reply_markup=InlineKeyboardMarkup(out[1]),
        ),
    )




@app.on_callback_query(filters.regex("hamo1"))
async def hamo1(_, CallbackQuery):
    await CallbackQuery.answer("گەڕانەوە ...")
    out = start_pannel()
    await CallbackQuery.edit_message_text(
        text=f"سوپاس بۆ ئەوەی منم لە ژوورەوە بوو  {CallbackQuery.message.chat.title}.\n{MUSIC_BOT_NAME} ئیستا چاڵاکە.\n\nبۆ هەر هاوکاری و یارمەتییەک، پشکنین بۆ گرووپ و کەناڵی پشتیوانیمان بکرێت.",
        reply_markup=InlineKeyboardMarkup(out[1]),
    )


@app.on_callback_query(filters.regex("settingm"))
async def settingm(_, CallbackQuery):
    await CallbackQuery.answer("ڕێکخستنی گروپ ...")
    text, buttons = setting_markup()
    c_title = CallbackQuery.message.chat.title
    c_id = CallbackQuery.message.chat.id
    chat_id = CallbackQuery.message.chat.id
    _check = await get_assistant(c_id, "assistant")
    if not _check:
        assis = {
            "volume": 100,
        }
        await save_assistant(c_id, "assistant", assis)
        volume = 100
    else:
        volume = _check["volume"]
    await CallbackQuery.edit_message_text(
        text=f"{text}\n\n**گرووپ:** {c_title}\n**ناسنامەی گروپ:** {c_id}\n**قەبارەی سەوت:** {volume}%",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("EVE"))
@ActualAdminCB
async def EVE(_, CallbackQuery):
    checking = CallbackQuery.from_user.username
    text, buttons = usermarkup()
    chat_id = CallbackQuery.message.chat.id
    is_non_admin = await is_nonadmin_chat(chat_id)
    if not is_non_admin:
        await CallbackQuery.answer("گۆڕانگاری هەڵگیرا")
        await add_nonadmin_chat(chat_id)
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\nمۆدی فەرمانەکانی بەڕێوەبەرەکان بۆ هەموو کەسێک \n\n ئێستا هەرکەسێک لەم گروپە ئامادەبێت دەتوانێت باز بدات، بوەستێت، دەستپێبکاتەوە، مۆسیقا بوەستێنێت.\n\n گۆڕانکاریەکان ئەنجام دەدرێت بە @{checking}",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        await CallbackQuery.answer(
            "مۆدی فەرمانەکان پێشتر دانراوە بۆ هەموو کەسێک", show_alert=True
        )


@app.on_callback_query(filters.regex("AMS"))
@ActualAdminCB
async def AMS(_, CallbackQuery):
    checking = CallbackQuery.from_user.username
    text, buttons = usermarkup()
    chat_id = CallbackQuery.message.chat.id
    is_non_admin = await is_nonadmin_chat(chat_id)
    if not is_non_admin:
        await CallbackQuery.answer(
            "مۆدی فەرمانەکان هەر ئێستا دانراوە بۆ بەڕێوەبەرەکان تەنها", show_alert=True
        )
    else:
        await CallbackQuery.answer("گۆرانکاری هەڵگیران")
        await remove_nonadmin_chat(chat_id)
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\nمۆدی فەرمانەکان ڕێک بخە بۆ بەڕێوەبەرەکان \n\n ئێستا تەنها ئەو بەڕێوەبەرانەی لەم گرووپەدا ئامادەن دەتوانن باز بدەن، بوەستن، دەستپێکردنەوە، وەستاندنی مووزیکەکان. \n\n گۆڕانکاریەکان ئەنجام دراوە بە @{checking}",
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@app.on_callback_query(
    filters.regex(
        pattern=r"^(AQ|AV|AU|Dashboard|HV|LV|MV|HV|VAM|Custommarkup|PTEN|MTEN|PTF|MTF|PFZ|MFZ|USERLIST|UPT|CPT|RAT|DIT)$"
    )
)
async def start_markup_check(_, CallbackQuery):
    command = CallbackQuery.matches[0].group(1)
    c_title = CallbackQuery.message.chat.title
    c_id = CallbackQuery.message.chat.id
    chat_id = CallbackQuery.message.chat.id
    if command == "AQ":
        await CallbackQuery.answer("پێشتر لە باشترین کوالێتی دا", show_alert=True)
    if command == "AV":
        await CallbackQuery.answer("ڕێکخستنی بۆت ...")
        text, buttons = volmarkup()
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**گروپ:** {c_title}\n**ناسنامەی گروپ:** {c_id}\n**قەبارەی سەوت:** {volume}%\n**کواڵێتی دەنگ:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "AU":
        await CallbackQuery.answer("ڕێکخستنی بۆت ...")
        text, buttons = usermarkup()
        is_non_admin = await is_nonadmin_chat(chat_id)
        if not is_non_admin:
            current = "Admins Only"
        else:
            current = "Everyone"
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**گروپ:** {c_title}\n\nئێستا کێ دەتوانێت بەکاری بهێنێت {MUSIC_BOT_NAME}:- **{current}**\n\n**⁉️ئەمە چیه ?**\n\n**👥 هەموکەس :-**هەمو کەس دەتوانێ {MUSIC_BOT_NAME} بەکاربێنی لە فەرمانەکانی (skip, pause, resume هتد) لەم گرووپە.\n\n**🙍 تەنیا بەڕێوەبەر :-**  تەنیا بەڕێوەبەر و ئەندامی تایبەت ئەتوانێ بەکاربێنی  {MUSIC_BOT_NAME}.",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "Dashboard":
        await CallbackQuery.answer("زانیاری...")
        text, buttons = dashmarkup()
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**گروپ:** {c_title}\n**ناسنامەی گروپ:** {c_id}\n**قەبارەی سەوت:** {volume}%\n\nپشکنینی {MUSIC_BOT_NAME} ئامارەکانی سیستەم لە داشبۆرد لێرە! کرداری زیاتر زۆر زوو زیاد دەکات! بەردەوامبە لە پشکنینی کەناڵی پشتگیری .",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "Custommarkup":
        await CallbackQuery.answer("ڕێکخستنی بۆت ...")
        text, buttons = custommarkup()
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**گروپ:** {c_title}\n**ناسنامەی گروپ:** {c_id}\n**قەبارەی سەوت:** {volume}%\n**کواڵێتی دەنگ:** باشترینە",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "LV":
        assis = {
            "volume": 25,
        }
        volume = 25
        try:
            await hama.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ڕێکخستنی گۆڕانکاریەکانی دەنگ  ...")
        except:
            return await CallbackQuery.answer("چاتی دەنگی چالاک نیە...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**گروپ:** {c_title}\n**ناسنامەی گروپ:** {c_id}\n**قەبارەی دەنگ:** {volume}%\n**کواڵیتی دەنگ:** باشترینی بنەڕەت",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MV":
        assis = {
            "volume": 50,
        }
        volume = 50
        try:
            await hama.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ڕێکخستنی گۆڕانکاریەکانی دەنگ  ...")
        except:
            return await CallbackQuery.answer("چاتی دەنگی نەکراوەتەوە")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**گروپ:** {c_title}\n**ناسنامەی گروپ:** {c_id}\n**قەبارەی دەنگ:** {volume}%\n**کواڵێتی دەنگ:** باشترینی بنەڕەت",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "HV":
        assis = {
            "volume": 100,
        }
        volume = 100
        try:
            await hama.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ڕێکخستنی گۆڕانکاریەکانی دەنگ  ...")
        except:
            return await CallbackQuery.answer("چاتی دەنگی چالاک نیە...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**گروپ:** {c_title}\n**ناسنامەی گروپ:** {c_id}\n**قەبارەی دەنگ:** {volume}%\n**جۆری دەنگ:** باشترین بنەڕەت",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "VAM":
        assis = {
            "volume": 200,
        }
        volume = 200
        try:
            await hama.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ڕێکخستنی گۆڕانکاریەکانی دەنگ  ...")
        except:
            return await CallbackQuery.answer("چاتی دەنگی چالاک نیە...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**گروپ:** {c_title}\n**ناسنامەی گروپ:** {c_id}\n**قەبارەی دەنگ:** {volume}%\n**جۆری دەنگ:** باشترین بنەڕەت",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PTEN":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 10
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await hama.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ڕێکخستنی گۆڕانکاریەکانی دەنگ  ...")
        except:
            return await CallbackQuery.answer("چاتی دەنگی چالاک نیە...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**گروپ:** {c_title}\n**ناسنامەی گروپ:** {c_id}\n**قەبارەی دەنگ:** {volume}%\n**جۆری دەنگ:** باشترین بنەڕەت",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MTEN":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 10
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await hama.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ڕێکخستنی گۆڕانکاریەکانی دەنگ  ...")
        except:
            return await CallbackQuery.answer("چاتی دەنگی چاڵاک نیە...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**گروپ:** {c_title}\n**ناسنامەی گروپ:** {c_id}\n**قەبارەی دەنگ:** {volume}%\n**جۆری دەنگ:** باشترین بنەڕەت",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PTF":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 25
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await hama.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ڕێکخستنی گۆڕانکاریەکانی دەنگ  ...")
        except:
            return await CallbackQuery.answer("چاتی دەنگی چاڵاک نیە...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**گروپ:** {c_title}\n**ناسنامەی گروپ:** {c_id}\n**قەبارەی ەوت:** {volume}%\n**جۆری دەنگ:** باشترینی بنەڕەت",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MTF":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 25
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await hama.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ڕێکخستنی گۆڕانکاریەکانی دەنگ ...")
        except:
            return await CallbackQuery.answer("چاتی دەنگی چالاک نیە...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**گروپ:** {c_title}\n**ناسنامەی گروپ:** {c_id}\n**قەبارەی سەوت:** {volume}%\n**جۆری دەنگ:** باشترین بنەڕەت",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PFZ":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 50
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await hama.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ڕێکخستنی گۆڕانکاریەکانی دەنگ  ...")
        except:
            return await CallbackQuery.answer("چاتی دەنگی چاڵاک نیە...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**ناو:** {c_title}\n**ناسنامەی گروپ:** {c_id}\n**قەبارەی سەوت:** {volume}%\n**جۆری دەنگ:** باشترین بنەڕەت",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MFZ":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 50
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await hama.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("ڕێکخستنی گۆڕانکاریەکانی دەنگ ...")
        except:
            return await CallbackQuery.answer("چاتی دەنگی چاڵاک نیە ...")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**گروپ:** {c_title}\n**ناسنامەی گروپ:** {c_id}\n**قەبارەی سەوت:** {volume}%\n**جۆری دەنگ:** باشترین بنەڕەت",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "USERLIST":
        await CallbackQuery.answer("بەکارهێنەرانی ئاوت!")
        text, buttons = usermarkup()
        _playlist = await get_authuser_names(CallbackQuery.message.chat.id)
        if not _playlist:
            return await CallbackQuery.edit_message_text(
                text=f"{text}\n\nهیچ بەکارهێنەرێکی ڕێپێدراو نەدۆزرایەوە n\n\ تۆ دەتوانیت ڕێگە بە هیچ بەڕێوەبەرێک بدەیت کە فەرمانەکانی بەڕێوەبەرەکەم بەکاربێنێت بە /auth و سڕینەوە بە بەکارهێنانی /unauth",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        else:
            j = 0
            await CallbackQuery.edit_message_text(
                "پکشنیک بۆ ئەندامە تایبەتەکان... تکایە چاوەڕوان بە"
            )
            msg = f"**لیستی ئەندامی تایبەت[AUL]:**\n\n"
            for note in _playlist:
                _note = await get_authuser(
                    CallbackQuery.message.chat.id, note
                )
                user_id = _note["auth_user_id"]
                user_name = _note["auth_name"]
                admin_id = _note["admin_id"]
                admin_name = _note["admin_name"]
                try:
                    user = await app.get_users(user_id)
                    user = user.first_name
                    j += 1
                except Exception:
                    continue
                msg += f"{j}➤ {user}[`{user_id}`]\n"
                msg += f"    ┗ زیادکراوە لەلایەن:- {admin_name}[`{admin_id}`]\n\n"
            await CallbackQuery.edit_message_text(
                msg, reply_markup=InlineKeyboardMarkup(buttons)
            )
    if command == "UPT":
        bot_uptimee = int(time.time() - bot_start_time)
        Uptimeee = f"{get_readable_time((bot_uptimee))}"
        await CallbackQuery.answer(
            f"بۆت کاتی نوێکاری: {Uptimeee}", show_alert=True
        )
    if command == "CPT":
        cpue = psutil.cpu_percent(interval=0.5)
        await CallbackQuery.answer(
            f"Bot's Cpu Usage: {cpue}%", show_alert=True
        )
    if command == "RAT":
        meme = psutil.virtual_memory().percent
        await CallbackQuery.answer(
            f"Bot's Memory Usage: {meme}%", show_alert=True
        )
    if command == "DIT":
        diske = psutil.disk_usage("/").percent
        await CallbackQuery.answer(
            f"Amort Disk Usage: {diske}%", show_alert=True
        )
