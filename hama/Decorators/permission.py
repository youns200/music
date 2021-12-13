from typing import Dict, List, Union

from hama import BOT_ID, app


def PermissionCheck(mystic):
    async def wrapper(_, message):
        a = await app.get_chat_member(message.chat.id, BOT_ID)
        if a.status != "administrator":
            return await message.reply_text(
                "پێویستە بە چەند مۆڵەتێک بەڕێوەبەر بم:\n"
                + "\n- **can_manage_voice_chats:** بۆ دەسکاری کردنی چاتی دەنگی"
                + "\n- **can_delete_messages:** سڕینەوەی چات"
                + "\n- **can_invite_users**: بۆ بانگێشتکردنی یاریدەدەر بۆ چات کردن."
            )
        if not a.can_manage_voice_chats:
            await message.reply_text(
                "من مۆڵەتی پێویستم نیە بۆ ئەنجامدانی ئەم کردارە."
                + "\n**مۆڵەت:** __MANAGE VOICE CHATS__"
            )
            return
        if not a.can_delete_messages:
            await message.reply_text(
                "من مۆڵەتی پێویستم نیە بۆ ئەنجامدانی ئەم کردارە.."
                + "\n**مۆڵەت:** __DELETE MESSAGES__"
            )
            return
        if not a.can_invite_users:
            await message.reply_text(
                "من مۆڵەتی پێویستم نیە بۆ ئەنجامدانی ئەم کردارە.."
                + "\n**مۆڵەت:** __INVITE USERS VIA LINK__"
            )
            return
        return await mystic(_, message)

    return wrapper
