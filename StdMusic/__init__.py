import asyncio
import logging
from config import API_ID, API_HASH, BOT_TOKEN, SESSION_STRING, OWNER_ID, SUDO_USERS

import re
import importlib.util
import pathlib
import shutil

# Ensure stdgram has required mime_types.txt before class definition evaluates
_spec = importlib.util.find_spec("stdgram")
if _spec and _spec.origin:
    _pkg_dir = pathlib.Path(_spec.origin).parent
    _target_mime = _pkg_dir / "mime_types.txt"
    if not _target_mime.exists():
        _local_mime = pathlib.Path(__file__).parent / "assets" / "mime_types.txt"
        if _local_mime.exists():
            try:
                shutil.copy(_local_mime, _target_mime)
            except Exception:
                pass

try:
    from stdgram import Client, filters
except (ImportError, Exception):
    from pyrogram import Client, filters

if not hasattr(filters, "regex"):
    def _regex(pattern):
        return filters.create(lambda _, __, q: bool(re.search(pattern, getattr(q, "data", "") or getattr(q, "text", ""))))
    filters.regex = _regex



try:
    from pytgcalls import PyTgCalls
except ImportError:
    PyTgCalls = None


logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("StdMusic")

try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)


# 1. Main Telegram Bot Client
app = Client(
    name="StdMusicBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# 2. Assistant Userbot Client (joins VC to stream audio/video)
userbot = (
    Client(
        name="StdAssistant",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION_STRING,
    )
    if SESSION_STRING
    else None
)

# 3. PyTgCalls Voice Chat Engine
pytgcalls = PyTgCalls(userbot) if userbot else None

# Bot and Assistant metadata holders
BOT_ID = 0
BOT_NAME = "StdMusic"
BOT_USERNAME = ""
ASS_ID = 0
ASS_NAME = "StdAssistant"
ASS_USERNAME = ""
