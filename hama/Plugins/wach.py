from pyrogram import filters

from hama import LOG_GROUP_ID, OWNER_ID, SUDOERS, app
from hama.Database import is_gbanned_user, is_on_off


@app.on_message(filters.private & ~filters.user(SUDOERS))
async def bot_forward(client, message):
    if await is_on_off(5):
        if message.text == "/start":
            return
        try:
            await app.forward_messages(
                chat_id=LOG_GROUP_ID,
                from_chat_id=message.from_user.id,
                message_ids=message.message_id,
            )
        except Exception as err:
            print(err)
            return
    else:
        return


chat_watcher_group = 5


@app.on_message(group=chat_watcher_group)
async def chat_watcher_func(_, message):
    try:
        userid = message.from_user.id
    except Exception:
        return
    checking = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    if await is_gbanned_user(userid):
        try:
            await message.chat.ban_member(userid)
        except Exception:
            return
        await message.reply_text(
            f"{checking} ببوورە تۆ سزادراویت تکای پەیوەندی بە داڕێژەی بۆت یان بەڕێوەبەرەکانی بکە بۆ لادانی سزات."
        )
