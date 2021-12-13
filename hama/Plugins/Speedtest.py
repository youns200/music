import os

import speedtest
import wget
from pyrogram import Client, filters
from pyrogram.types import Message

from hama import BOT_ID, SUDOERS, app

__MODULE__ = "خێرای بۆت"
__HELP__ = """

/speedtest 
- بۆ پشکنینی خێرای بۆت.

"""


def bytes(size: float) -> str:
    """humanize size"""
    if not size:
        return ""
    power = 1024
    t_n = 0
    power_dict = {0: " ", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        t_n += 1
    return "{:.2f} {}B".format(size, power_dict[t_n])


@app.on_message(filters.command("speedtest") & ~filters.edited)
async def statsguwid(_, message):
    m = await message.reply_text("پشکنینی خێرای بۆت")
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = await m.edit("داگرتنی خێرای بۆت")
        test.download()
        m = await m.edit("بارکردنی خێرای بۆت")
        test.upload()
        test.results.share()
        result = test.results.dict()
    except Exception as e:
        return await m.edit(e)
    m = await m.edit("هاوبەشکردنی خێرای بۆت")
    path = wget.download(result["share"])

    output = f"""**لیستی خێرای**
    
<u>**Client:**</u>
**__ISP:__** {result['client']['isp']}
**__وڵات:__** {result['client']['country']}
  
<u>**سرێڤەر:**</u>
**__ناو:__** {result['server']['name']}
**__وڵات:__** {result['server']['country']}, {result['server']['cc']}
**__سپۆنسەر:__** {result['server']['sponsor']}
**__لاتینس:__** {result['server']['latency']}  
**__پینگ:__** {result['ping']}"""
    msg = await app.send_photo(
        chat_id=message.chat.id, photo=path, caption=output
    )
    os.remove(path)
    await m.delete()
