from os import getenv

from dotenv import load_dotenv

load_dotenv()

# VARS

get_queue = {}
STRING = getenv("STRING_SESSION", "AgAFMtyBFABiSiyyCEKgl6gj8qT91g8OIoboTFzpLWXnoT2OnIrapcNIvZrm8MYTwUbriWYGnJDXW9AG_39NJ8ERSKJqHOp1LPd8wvgkimfJQdCv7Z2AxmE6x2bfoC3lIn8TYYJzPt02nVMzUQc6jcG85EmLAuVnCZFA6X1gjYKhw7dH2w8rlkte03KEUfx3I27PP1pU6XZD_ZQXBLhMcaIOglTpLNonoPE6ccBWEqzRs7ENG3kXW-CG6nj2bFLmaWmY6RjhhIgRS9G9yiVDJA6Hpuyv-U-x3pS9JG6QTOsCdMK_xPelUYWRisbnZDEYrrzN3CaASjJZv-0hchq4bA5LaOkGgwA")
BOT_TOKEN = getenv("BOT_TOKEN", "2100441086:AAEGGfcEENlB_xd2wXTNq1Elrrm5v1c5Ym8")
API_ID = int(getenv("API_ID", "6699478"))
API_HASH = getenv("API_HASH", "28e67d90d53ce22e01d330141824b1da")
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", "60"))
ASSISTANT_PREFIX = list(getenv("ASSISTANT_PREFIX", ".").split())
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://music:music@cluster0.jodqj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "511311707").split()))
OWNER_ID = list(map(int, getenv("OWNER_ID", "511311707").split()))
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", "-1001665697505"))
MUSIC_BOT_NAME = getenv("MUSIC_BOT_NAME", "Music Bot")

#----
if str(getenv("SUPPORT_CHANNEL")).strip() == "":
    SUPPORT_CHANNEL = None
else:
    SUPPORT_CHANNEL = str(getenv("SUPPORT_CHANNEL"))
if str(getenv("SUPPORT_GROUP")).strip() == "":
    SUPPORT_GROUP = None
else:
    SUPPORT_GROUP = str(getenv("SUPPORT_GROUP"))
#-------------
if str(getenv("CHANNEL")).strip() == "":
    CHANNEL = None
else:
    CHANNEL = str(getenv("CHANNEL"))
if str(getenv("NAMECH")).strip() == "":
    NAMECH = None
else:
    NAMECH = str(getenv("NAMECH"))
#-----
if str(getenv("MUST_JOIN")).strip() == "":
    MUST_JOIN = None
else:
    MUST_JOIN = str(getenv("MUST_JOIN"))

