import asyncio
import os

from pyrogram import Client, filters
from pyrogram.types import Message

from hama import SUDOERS, app
from config import MUSIC_BOT_NAME
from hama.Database import get_gbans_count, get_served_chats, get_served_user


@app.on_message(filters.command("admin") & filters.user(SUDOERS))
async def admin(_, message):
      await message.reply_text(
               f""" **سلاوو بەڕێوەبەر**
ئەم فەرمانانەی ئیستا بۆتۆ بەردەستن -
__فەرمانەکانی دەرکردن و بڵۆک کردن و دەرکردنی بۆت پێویستی بە ئایدی یان یوسەر نەیمی کەسەکە یان گروپەکە هەیە__ 
1- `/block` بۆ بڵۆک کردنی گروپ هەر گروپێک بتەوێ
2- `/unblock` بۆ لادانی بڵۆکی گروپەکەی سزات داوە
3- `/update` بۆ نوێ کردنەوەی بۆت
4- `/gban` بۆ دەرکردنی ئەندام لەهەموو گروپەکان
5- `/ungban` بۆ لادانی دەرکردن لەهەموو گروپەکان
6- `/broadcast` لەڕیپڵەی چات یان چات بنوسە لەگەڵی
7- `/broadcast_pin` لەڕیپڵەی چات یان چات بنوسە لەگەڵی
8- `/broadcast_pin_loud` لەڕیپڵەی چات یان چات بنوسە لەگەڵی
9- `/clean` بۆ سڕینەوەی فایڵەکان
10- `/restart` بۆ ڕستارت کردنەوەی بۆت
11- `/leavebot` بۆ دەرکردنی بۆت لەگروپێک بتەوێ
12- `/join` بۆ زیادکردنی یارمەتی دەر
13- `/leave` بۆ دەرکردنی یارمەتی دەر لەگروپەکان
"""
                )
@app.on_message(filters.command("stats") & filters.user(SUDOERS))
async def admin(_, message):
    chat_id = message.chat.id
    message = await message.reply_text(
        chat_id, "❖ Collecting Stats..."
    )
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_user())
    gbans_usertl = await get_gbans_count()
    tgm = f"""
📊 تۆمارەکانی [{MUSIC_BOT_NAME}]`:`
➥ **گرووپ چاتەکان** : `{served_chats}`
➥ **بەکارهێنەرەکان** : `{served_users}`
➥ **ئەندامی بانکراوو** : `{gbans_usertl}`
"""
    await message.edit(tgm, disable_web_page_preview=True)
