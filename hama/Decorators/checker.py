
from hama import BOT_USERNAME, LOG_GROUP_ID, app
from hama.Database import blacklisted_chats, is_gbanned_user, is_on_off


def checker(mystic):
    async def wrapper(_, message):
        if message.sender_chat:
            return await message.reply_text(
                "**تۆ __Anonymous Admin__ لەم گروپەی چات! گەڕانەوە بۆ ئەژمێری بەکارهێنەر لە مافەکانی بەڕێوەبەر**."
            )
        blacklisted_chats_list = await blacklisted_chats()
        if message.chat.id in blacklisted_chats_list:
            await message.reply_text(
                f"**لیستی ڕەش **\n\nچاتەکەت لەلایەن بەکارهێنەرانی سۆدۆوە لیستی ڕەشی لێدراوە. پرسیار لە هەر __SUDO USER__ بکە بۆ لیستی سپی. لیستی بەکارهێنەرانی Sudo بپشکنە [لێرەوە](https://t.me/{BOT_USERNAME}?start=sudolist)"
            )
            return await app.leave_chat(message.chat.id)
        if await is_on_off(1):
            if int(message.chat.id) != int(LOG_GROUP_ID):
                return await message.reply_text(
                    f"Bot is under Maintenance. Sorry for the inconvenience!"
                )
        if await is_gbanned_user(message.from_user.id):
            return await message.reply_text(
                f"**چاتەکەت لەلایەن بەکارهێنەرانی سۆدۆوە لیستی ڕەشی لێدراوە. پرسیار لە هەر __SUDO USER__ بکە بۆ لیستی سپی. لیستی بەکارهێنەرانی Sudo بپشکنە** [لێرەوە](https://t.me/{BOT_USERNAME}?start=sudolist)"
            )
        return await mystic(_, message)

    return wrapper


def checkerCB(mystic):
    async def wrapper(_, CallbackQuery):
        blacklisted_chats_list = await blacklisted_chats()
        if CallbackQuery.message.chat.id in blacklisted_chats_list:
            return await CallbackQuery.answer(
                "چاتێکی لیستی ڕەش", show_alert=True
            )
        if await is_on_off(1):
            if int(CallbackQuery.message.chat.id) != int(LOG_GROUP_ID):
                return await CallbackQuery.answer(
                    "بۆت لەژێر چاودێریدایە. ببورە بۆ ناتەبایی!",
                    show_alert=True,
                )
        if await is_gbanned_user(CallbackQuery.from_user.id):
            return await CallbackQuery.answer(
                "تۆ قەدەغەکراویت", show_alert=True
            )
        return await mystic(_, CallbackQuery)

    return wrapper
