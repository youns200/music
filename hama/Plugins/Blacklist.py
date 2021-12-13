from pyrogram import Client, filters
from pyrogram.types import Message

from hama import SUDOERS, app
from hama.Database import blacklist_chat, blacklisted_chats, whitelist_chat

__MODULE__ = " بڵۆک"
__HELP__ = """


/blacklistedchat 
- بۆ پشکینینی لیستی بڵۆک کراوەکان.


**تێبینی:**
تەنیا بۆ بەڕێوەبەری بۆتە.


/blacklistchat [CHAT_ID] 
- بۆ بلۆک کردنی گروپ لە بۆتی گۆرانی وتن


/whitelistchat [CHAT_ID] 
- بۆ بڵۆک کردنی ئەندام لەگروپ چاتەکان

"""


@app.on_message(filters.command("blacklistchat") & filters.user(SUDOERS))
async def blacklist_chat_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "**Usage:**\n/blacklistchat [CHAT_ID]"
        )
    chat_id = int(message.text.strip().split()[1])
    if chat_id in await blacklisted_chats():
        return await message.reply_text("Chat is already blacklisted.")
    blacklisted = await blacklist_chat(chat_id)
    if blacklisted:
        return await message.reply_text(
            "Chat has been successfully blacklisted"
        )
    await message.reply_text("Something wrong happened, check logs.")


@app.on_message(filters.command("whitelistchat") & filters.user(SUDOERS))
async def whitelist_chat_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "**Usage:**\n/whitelistchat [CHAT_ID]"
        )
    chat_id = int(message.text.strip().split()[1])
    if chat_id not in await blacklisted_chats():
        return await message.reply_text("Chat is already whitelisted.")
    whitelisted = await whitelist_chat(chat_id)
    if whitelisted:
        return await message.reply_text(
            "Chat has been successfully whitelisted"
        )
    await message.reply_text("Something wrong happened, check logs.")


@app.on_message(filters.command("blacklistedchat"))
async def blacklisted_chats_func(_, message: Message):
    text = "**لیستی بڵۆکی گروپەکان:**\n\n"
    j = 0
    for count, chat_id in enumerate(await blacklisted_chats(), 1):
        try:
            title = (await app.get_chat(chat_id)).title
        except Exception:
            title = "Private"
        j = 1
        text += f"**{count}. {title}** [`{chat_id}`]\n"
    if j == 0:
        await message.reply_text("لە لیستی بڵۆک نیە")
    else:
        await message.reply_text(text)
