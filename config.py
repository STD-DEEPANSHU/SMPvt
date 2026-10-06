import os
import sys
from dotenv import load_dotenv

load_dotenv()


def _require(name: str) -> str:
    val = os.getenv(name, "").strip()
    if not val:
        # Default mock fallback for local checking, or exit in production
        return ""
    return val


def _int_list(name: str) -> list[int]:
    raw = os.getenv(name, "").strip()
    if not raw:
        return []
    return [int(x) for x in raw.split() if x.isdigit()]


# --- Telegram API Credentials ---
API_ID = int(os.getenv("API_ID", "1234567"))
API_HASH = os.getenv("API_HASH", "your_api_hash_here")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token_here")
OWNER_ID = int(os.getenv("OWNER_ID", "6073400587"))
SUDO_USERS = _int_list("SUDO_USERS")
if OWNER_ID and OWNER_ID not in SUDO_USERS:
    SUDO_USERS.append(OWNER_ID)

# --- Assistant Client (Userbot for VC Voice Streams) ---
SESSION_STRING = os.getenv("SESSION_STRING", os.getenv("STRING_SESSION", "")).strip()

# --- Database & Cache ---
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/stdmusic").strip()

# --- Playback Configuration ---
DURATION_LIMIT = int(os.getenv("DURATION_LIMIT", "3600"))  # 60 minutes
AUTO_LEAVE_TIME = int(os.getenv("AUTO_LEAVE_TIME", "60"))  # Leave VC after 60s idle
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads")

# --- StdAPI Engine Configuration ---
STDAPI_BASE_URL = os.getenv("STDAPI_BASE_URL", "https://stdapi.vercel.app").strip()
STDAPI_KEY = os.getenv("STDAPI_KEY", "").strip()

# --- Bot Visuals & Identity ---
BOT_NAME = os.getenv("BOT_NAME", "StdMusic")
START_IMG_URL = os.getenv("START_IMG_URL", "https://graph.org/file/f4b16beae1579beab1479.jpg")
SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "https://t.me/TeamStdNetwork")
SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", "https://t.me/TeamStdNetwork")
