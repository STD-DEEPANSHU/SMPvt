import asyncio
import logging
import os
import re
import sys
import types
import importlib.util
import pathlib
import shutil

from config import API_ID, API_HASH, BOT_TOKEN, SESSION_STRING, OWNER_ID, SUDO_USERS

# 1. Ensure stdgram has required mime_types.txt before class definition evaluates
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

# 2. Setup Pyrogram Compatibility Bridge for PyTgCalls using StdGram
if "pyrogram" not in sys.modules:
    try:
        import stdgram
        import stdgram.client
        import stdgram.raw
        import stdgram.raw.base
        import stdgram.raw.types
        import stdgram.raw.functions
        import stdgram.raw.functions.phone
        import stdgram.raw.functions.auth
        import stdgram.raw.functions.channels
        import stdgram.raw.functions.messages
        import stdgram.raw.functions.upload
        import stdgram.errors
        import stdgram.types
        import stdgram.session

        for _mod_name, _mod in list(sys.modules.items()):
            if _mod_name.startswith("stdgram"):
                sys.modules["pyrogram" + _mod_name[7:]] = _mod

        sys.modules["pyrogram"].__version__ = "2.3.69"

        class _PyrogramSubmoduleFinder:
            @classmethod
            def find_spec(cls, fullname, path=None, target=None):
                if fullname.startswith("pyrogram."):
                    std_name = "stdgram" + fullname[len("pyrogram"):]
                    if std_name in sys.modules:
                        mod = sys.modules[std_name]
                        sys.modules[fullname] = mod
                        return getattr(mod, "__spec__", None)
                    try:
                        import importlib
                        mod = importlib.import_module(std_name)
                        sys.modules[fullname] = mod
                        return getattr(mod, "__spec__", None)
                    except Exception:
                        pass
                return None

        sys.meta_path.insert(0, _PyrogramSubmoduleFinder)
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

# 3. Patch PyTgCalls to accept StdGram as valid MTProto Client
try:
    from pytgcalls import PyTgCalls
    try:
        from pytgcalls.mtproto.bridged_client import BridgedClient
        _orig_pkg_name = BridgedClient.package_name

        def _bridged_pkg_name(obj):
            name = _orig_pkg_name(obj)
            if name == "stdgram":
                return "pyrogram"
            return name

        BridgedClient.package_name = staticmethod(_bridged_pkg_name)
    except Exception:
        pass

    try:
        from pytgcalls.mtproto.mtproto_client import MtProtoClient
        from pytgcalls.mtproto.pyrogram_client import PyrogramClient
        _orig_mtproto_init = MtProtoClient.__init__

        def _bridged_mtproto_init(self, cache_duration, client):
            pkg = BridgedClient.package_name(client)
            if pkg in ("pyrogram", "stdgram"):
                self.package_name = "pyrogram"
                self._bind_client = PyrogramClient(cache_duration, client)
            else:
                _orig_mtproto_init(self, cache_duration, client)

        MtProtoClient.__init__ = _bridged_mtproto_init
    except Exception:
        pass
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
pytgcalls = None
if userbot and PyTgCalls:
    try:
        pytgcalls = PyTgCalls(userbot)
        logger.info("PyTgCalls voice chat engine initialized successfully with StdGram client.")
    except Exception as e:
        logger.error(f"Failed to initialize PyTgCalls engine: {e}", exc_info=True)

# Bot and Assistant metadata holders
BOT_ID = 0
BOT_NAME = "StdMusic"
BOT_USERNAME = ""
ASS_ID = 0
ASS_NAME = "StdAssistant"
ASS_USERNAME = ""
