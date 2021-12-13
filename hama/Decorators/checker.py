from hama import BOT_USERNAME, LOG_GROUP_ID, app
from hama.Database import blacklisted_chats, is_gbanned_user, is_on_off


def checker(mystic):
    async def wrapper(_, message):
        if message.sender_chat:
            return await message.reply_text(
                "تۆ وەرگری __Anonymous Admin__ لەم گروپی چاتەدا!\nگەڕانەوە بۆ ئەژمێری بەکارهێنەر لە مافەکانی بەڕێوەبەر."
            )
        blacklisted_chats_list = await blacklisted_chats()
        if message.chat.id in blacklisted_chats_list:
            await message.reply_text(
                f"**بڵۆک کراوە چاتە**\nچاتەکەت لەلایەن بەکارهێنەرانی سۆدۆوە لیستی ڕەش کراوە. پرسیار بکە لە هەر __ SUDO User __ بۆ لیستی سپی. لیستی بەکارهێنەرانی Sudo بپشکنە\n [ئێرە دابگرە](https://t.me/{BOT_USERNAME}?start=sudolist)"
            )
            return await app.leave_chat(message.chat.id)
        if await is_on_off(1):
            if int(message.chat.id) != int(LOG_GROUP_ID):
                return await message.reply_text(
                    f"‌بۆت لەژێر چاودێریدایە. ببورە بۆ ناتەبای!"
                )
        if await is_gbanned_user(message.from_user.id):
            return await message.reply_text(
                f"**بەکارهێنەرە سزادراوا**\n\nتۆ لە بەکارهێنانی بۆت گێگابایت پرسیار لە هەر __SUDO USER__ بۆ لادانی سزا.\nلیستی بەکارهێنەرانی Sudo بپشکنە [ئێرە دابگرە](https://t.me/{BOT_USERNAME}?start=sudolist)"
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
                "تۆ سزادراوی", show_alert=True
            )
        return await mystic(_, CallbackQuery)

    return wrapper
