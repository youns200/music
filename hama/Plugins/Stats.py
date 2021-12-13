import asyncio
import json
import logging
import platform
import re
import socket
import time
import uuid
from datetime import datetime
from sys import version as pyver

import psutil
from pyrogram import Client
from pyrogram import __version__ as pyrover
from pyrogram import filters
from pyrogram.types import Message
from pymongo import MongoClient
from config import MONGO_DB_URI
from hama import (BOT_ID, MUSIC_BOT_NAME, SUDOERS, app, boottime,
                   userbot)
from hama.Database import get_gbans_count, get_served_chats, get_sudoers
from hama.Inline import (stats1, stats2, stats3, stats4, stats5, stats6,
                          stats7)
from hama.Plugins import ALL_MODULES
from hama.Utilities.ping import get_readable_time

__MODULE__ = "تۆماری بۆت"
__HELP__ = """


/stats 
- بۆ دەست کەوتنی زانیاری لەسەر بۆت.
- بۆ دەست کەوتنی زانیاری لەسەر MongoDb , Assistant, System etc
"""


async def bot_sys_stats():
    bot_uptime = int(time.time() - boottime)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    stats = f"""
**کاتی نوێکار:** {get_readable_time((bot_uptime))}
**کوپ:** {cpu}%
**ڕام:** {mem}%
**دیسک: **{disk}%"""
    return stats


@app.on_message(filters.command("stats") & ~filters.edited)
async def gstats(_, message):
    start = datetime.now()
    try:
        await message.delete()
    except:
        pass
    uptime = await bot_sys_stats()
    response = await message.reply_photo(
        photo="Utils/Query.jpg", caption="بەدەستهێنانی ئامارەکان!")
    end = datetime.now()
    resp = (end - start).microseconds / 1000
    smex = f"""
[•]<u>** ئامارەکان**</u>
    
Ping: `⚡{resp} ms`
{uptime}
    """
    await response.edit_text(smex, reply_markup=stats1)
    return


@app.on_callback_query(
    filters.regex(
        pattern=r"^(sys_stats|sto_stats|bot_stats|Dashboard|mongo_stats|gen_stats|assis_stats|wait_stats)$"
    )
)
async def stats_markup(_, CallbackQuery):
    command = CallbackQuery.matches[0].group(1)
    if command == "sys_stats":
        await CallbackQuery.answer("بەدەستهێنانی ئامارەکانی سیستەم...", show_alert=True)
        sc = platform.system()
        arch = platform.machine()
        ram = (
            str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"
        )
        bot_uptime = int(time.time() - boottime)
        uptime = f"{get_readable_time((bot_uptime))}"
        smex = f"""
[•]<u>**ئامارەکانی سیستەم**</u>

**کاتی نوێکاری:** {uptime}
**دۆخی سیستەم:** Online
**پلاتفۆڕم:** {sc}
**تەلارسازی:** {arch}
**ڕام:** {ram}
**پایتۆن ڤێر:** {pyver.split()[0]}
**پیرۆگرام ڤێر:** {pyrover}"""
        await CallbackQuery.edit_message_text(smex, reply_markup=stats2)
    if command == "sto_stats":
        await CallbackQuery.answer(
            "دەستکەوتنی ئامارەکانی کۆگا...", show_alert=True
        )
        hdd = psutil.disk_usage("/")
        total = hdd.total / (1024.0 ** 3)
        total = str(total)
        used = hdd.used / (1024.0 ** 3)
        used = str(used)
        free = hdd.free / (1024.0 ** 3)
        free = str(free)
        smex = f"""
[•]<u>**ئامارەکانی کۆگا**</u>

**خەزنکردنی Avail:** {total[:4]} GiB 
**خەزن کردن بەکارهاتووە: **{used[:4]} GiB
**کۆگا لای چەپ:** {free[:4]} GiB"""
        await CallbackQuery.edit_message_text(smex, reply_markup=stats3)
    if command == "bot_stats":
        await CallbackQuery.answer("بەدەستهێنانی ئامارەکانی بۆت...", show_alert=True)
        served_chats = []
        chats = await get_served_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
        blocked = await get_gbans_count()
        sudoers = await get_sudoers()
        modules_loaded = len(ALL_MODULES)
        j = 0
        for count, user_id in enumerate(sudoers, 0):
            try:
                user = await app.get_users(user_id)
                j += 1
            except Exception:
                continue
        smex = f"""
[•]<u>**بۆت ئامارەکان**</u>

**مۆدیوولەکان بارکراوە:** {modules_loaded}
**بەکارهێنەرانی GBanned:** {blocked}
**بەکارهێنەرانی Sudo:** {j}
**چاتەکانی خزمەت کرد:** {len(served_chats)}"""
        await CallbackQuery.edit_message_text(smex, reply_markup=stats4)
    if command == "mongo_stats":
        await CallbackQuery.answer(
            "بەدەستهێنانی ئامارەکانی MongoDB...", show_alert=True
        )
        db = pymongodb
        call = db.command("dbstats")
        database = call["db"]
        datasize = call["dataSize"] / 1024
        datasize = str(datasize)
        storage = call["storageSize"] / 1024
        objects = call["objects"]
        collections = call["collections"]
        status = db.command("serverStatus")
        query = status["opcounters"]["query"]
        mver = status["version"]
        mongouptime = status["uptime"] / 86400
        mongouptime = str(mongouptime)
        provider = status["repl"]["tags"]["provider"]
        smex = f"""
[•]<u>**ئامارەکانی MongoDB**</u>

**کاتینوێکاری Mongo:** {mongouptime[:4]} Days
**وەشان:** {mver}
**داتابەیسی:** {database}
**دابینکەر:** {provider}
**قەبارەی DB:** {datasize[:6]} Mb
**خەزنکردنی:** {storage} Mb
**کۆکراوەکان:** {collections}
**کلیلەکان:** {objects}
**کۆی کیوریەکان:** `{query}`"""
        await CallbackQuery.edit_message_text(smex, reply_markup=stats5)
    if command == "assis_stats":
        await CallbackQuery.answer(
            "دەستکەوتنی یاریدەدەری ئامارەکان...", show_alert=True
        )
        await CallbackQuery.edit_message_text(
            "دەستکەوتنی یاریدەدەری ئامارەکان. تکایە چاوەڕوان بە...", reply_markup=stats7
        )
        groups_ub = channels_ub = bots_ub = privates_ub = total_ub = 0
        async for i in userbot.iter_dialogs():
            t = i.chat.type
            total_ub += 1
            if t in ["supergroup", "group"]:
                groups_ub += 1
            elif t == "channel":
                channels_ub += 1
            elif t == "bot":
                bots_ub += 1
            elif t == "private":
                privates_ub += 1

        smex = f"""
[•]<u>ئامارەکانی یاری دەر</u>

**دیالۆگەکان:** {total_ub}
**گروپەکان:** {groups_ub} 
**کەناڵەکان:** {channels_ub} 
**بۆتەکەکان:** {bots_ub}
**ئەندامەکان:** {privates_ub}"""
        await CallbackQuery.edit_message_text(smex, reply_markup=stats6)
    if command == "gen_stats":
        start = datetime.now()
        uptime = await bot_sys_stats()
        await CallbackQuery.answer(
            " بەدەستهێنانی ئامارە گشتیەکان...", show_alert=True
        )
        end = datetime.now()
        resp = (end - start).microseconds / 1000
        smex = f"""
[•]<u>ئامارە گشتیەکان</u>

**پینگ:** `⚡{resp} ms`
{uptime}"""
        await CallbackQuery.edit_message_text(smex, reply_markup=stats1)
    if command == "wait_stats":
        await CallbackQuery.answer()
