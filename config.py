from os import getenv

from dotenv import load_dotenv

load_dotenv()

# VARS

get_queue = {}
STRING = getenv("STRING_SESSION", "AgAeQXjYUNrcZ1_gKt-4iyIW9YPMrzUXhNyP2C9qK8iRa7uc8IKR_a09AHcBkrNjOPO5cmyEqhc180s6TvIB4AkXSiujJeF5L1FKJrvMhAMI1esyBf28MWDsh718aVRWcHmfqsSLisGQMNYr37h2TF31PEALD6_dB1L16QXOR8be7gpLlhGppa2cUJ0Lj9dKQNc3psSrV2a5548OLEbf5V-MzzLO0dVOWx5fuPtPwg1oJWJBSv5SStT8_LiObxbLdlF0iy8fKded82virFdijCg7HdjbfD9I9N6SUTqWtP51Rzb3NlmO37PzojZMU8drJkoqlAx6WHrfK_kictou4MQ0Z4b_4QA")
BOT_TOKEN = getenv("BOT_TOKEN", "2100441086:AAEGGfcEENlB_xd2wXTNq1Elrrm5v1c5Ym8")
API_ID = int(getenv("API_ID", "6699478"))
API_HASH = getenv("API_HASH", "28e67d90d53ce22e01d330141824b1da")
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", "1000"))
ASSISTANT_PREFIX = list(getenv("ASSISTANT_PREFIX", ".").split())
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://hamat:hamat@cluster0.i9wpi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "511311707").split()))
OWNER_ID = list(map(int, getenv("OWNER_ID", "511311707").split()))
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", "-1001665697505"))
MUSIC_BOT_NAME = getenv("MUSIC_BOT_NAME", "Music")


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

    
