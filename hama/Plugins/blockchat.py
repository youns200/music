from pyrogram import Client, filters
from pyrogram.types import Message

from hama import SUDOERS, app
from hama.Database import blacklist_chat, blacklisted_chats, whitelist_chat


@app.on_message(filters.command("block") & filters.user(SUDOERS))
async def blacklist_chat_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "**Usage:**\n/blacklistchat [CHAT_ID]"
        )
    chat_id = int(message.text.strip().split()[1])
    if chat_id in await blacklisted_chats():
        return await message.reply_text("پێشتر بڵۆک کراوە.")
    blacklisted = await blacklist_chat(chat_id)
    if blacklisted:
        return await message.reply_text(
            "بەسەرکەوتوی بڵۆک کرا"
        )
    await message.reply_text("ببوورە هەڵەڕوویدا")


@app.on_message(filters.command("unblock") & filters.user(SUDOERS))
async def whitelist_chat_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "**فرمان:**\n/unblock [CHAT_ID]"
        )
    chat_id = int(message.text.strip().split()[1])
    if chat_id not in await blacklisted_chats():
        return await message.reply_text("پێشتر لادراوە")
    whitelisted = await whitelist_chat(chat_id)
    if whitelisted:
        return await message.reply_text(
            "بەسەرکەوتوی لە لیستی بڵۆک لادرا"
        )
    await message.reply_text("هەڵەڕوویدا دواتر هەوڵبدە.")


@app.on_message(filters.command("blacklistedchat"))
async def blacklisted_chats_func(_, message: Message):
    text = "**لیستی گروپەکانی بڵۆک کراون:**\n\n"
    j = 0
    for count, chat_id in enumerate(await blacklisted_chats(), 1):
        try:
            title = (await app.get_chat(chat_id)).title
        except Exception:
            title = "Private"
        j = 1
        text += f"**{count}. {title}** [`{chat_id}`]\n"
    if j == 0:
        await message.reply_text("لیستی گروپەکان بڵۆک کراون بەتاڵە")
    else:
        await message.reply_text(text)
