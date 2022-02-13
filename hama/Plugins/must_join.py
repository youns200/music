from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
from config import MUST_JOIN
from hama import app, BOT_USERNAME

@app.on_message(~filters.edited & filters.incoming & filters.private, group=-1)
async def must_join_channel(bot: Client, msg: Message):
    if not MUST_JOIN:  # Not compulsory
        return
    try:
        try:
            await bot.get_chat_member(MUST_JOIN, msg.from_user.id)
        except UserNotParticipant:
            if MUST_JOIN.isalpha():
                link = "https://t.me/" + MUST_JOIN
            else:
                chat_info = await bot.get_chat(MUST_JOIN)
                link = chat_info.invite_link
            try:
                await msg.reply_text(
                    f"**ببوورە ئەزیزم  {mgs.from_user.mention} سەرەتا جۆینی کەناڵ بکە تاکوو بتوانی بۆت بەکاربێنی 🫀**",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("✨ جۆین ✨", url=link)]
                    ])
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"I'm not admin in the MUST_JOIN chat : {MUST_JOIN} !")

        
@app.on_message(filters.command(["help", f"help@{BOT_USERNAME}", "start", f"start@{BOT_USERNAME}", "play", f"play@{BOT_USERNAME}", "help", f"help@{BOT_USERNAME}", "skip", f"skip@{BOT_USERNAME}", "stop", f"stop@{BOT_USERNAME}", "end", f"end@{BOT_USERNAME}"]) & filters.group, group=-1)
async def must_join_channel(bot: Client, msg: Message):
    if not MUST_JOIN:  # Not compulsory
        return
    try:
        try:
            await bot.get_chat_member(MUST_JOIN, msg.from_user.id)
        except UserNotParticipant:
            if MUST_JOIN.isalpha():
                link = "https://t.me/" + MUST_JOIN
            else:
                chat_info = await bot.get_chat(MUST_JOIN)
                link = chat_info.invite_link
            try:
                await msg.reply_text(
                    f"**ببوورە ئەزیزم  {msg.from_user.mention} سەرەتا جۆینی کەناڵ بکە تاکوو بتوانی بۆت بەکاربێنی 🫀**",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("✨ جۆین ✨", url=link)]
                    ])
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"I'm not admin in the MUST_JOIN chat : {MUST_JOIN} !")
