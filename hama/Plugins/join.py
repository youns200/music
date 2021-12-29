import asyncio
from hama import chanel, app, db_mem
from pyrogram import Client
from pyrogram import filters
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, Message

from hama.Inline import join

async def handle_force_subscribe(_, message):
    try:
        invite_link = await app.create_chat_invite_link(int(hama.chanel))
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return 400
    try:
        user = await app.get_chat_member(int(hama.chanel), message.from_user.id)
        if user.status == "kicked":
            await app.send_message(
                chat_id=message.from_user.id,
                text="Sorry Sir, You are Banned. Contact My [Support Group](https://t.me/kurd_botschat).",
                parse_mode="markdown",
                disable_web_page_preview=True,
                reply_to_message_id=message.message_id,
            )
            return 400
    except UserNotParticipant:
        await app.send_message(
            chat_id=message.from_user.id,
            text="**Please Join My Updates Channel To Use Me!**\n\nDue to Overload, Only Channel Subscribers Can Use Me!",
            reply_markup=InlineKeyboardMarkup(join),
            parse_mode="markdown",
            reply_to_message_id=message.message_id,
        )
        return 400
    except Exception:
        await app.send_message(
            chat_id=message.from_user.id,
            text="Something Went Wrong. Contact My [Support Group](https://t.me/kurd_botschat).",
            parse_mode="markdown",
            disable_web_page_preview=True,
            reply_to_message_id=message.message_id,
        )
        return 400
