import asyncio
import os

from pyrogram import Client, filters
from pyrogram.types import Message

from hama import SUDOERS, app

@app.on_message(filters.command("admin") & filters.user(SUDOERS))
async def admin(_, message):
      await message.reply_text(
               f""" **سلاوو بەڕێوەبەر**
ئەم فەرمانانەی ئیستا بۆتۆ بەردەستن - 
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
12- ``
13- ``
"""
                )
