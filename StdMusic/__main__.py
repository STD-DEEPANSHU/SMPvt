import asyncio
import importlib
import logging
import sys

try:
    from stdgram import idle
except ImportError:
    from pyrogram import idle

from StdMusic import app, userbot, pytgcalls, BOT_NAME, logger
from StdMusic.plugins import ALL_PLUGINS
from config import OWNER_ID


async def main():
    logger.info("Initializing StdMusic...")

    # 1. Start Main Bot Client
    logger.info("Starting Telegram Bot client...")
    await app.start()
    bot_me = await app.get_me()
    logger.info(f"Bot started successfully as @{bot_me.username} ({bot_me.id})")

    # 2. Start Assistant Userbot if configured
    if userbot:
        logger.info("Starting Assistant Userbot client...")
        try:
            await userbot.start()
            ass_me = await userbot.get_me()
            logger.info(f"Assistant started as @{ass_me.username or 'Assistant'} ({ass_me.id})")
        except Exception as e:
            logger.warning(f"Could not start assistant userbot: {e}")

    # 3. Start PyTgCalls Voice Engine
    if pytgcalls:
        logger.info("Starting PyTgCalls Voice Chat Engine...")
        try:
            await pytgcalls.start()
            logger.info("PyTgCalls engine active and listening.")
        except Exception as e:
            logger.warning(f"PyTgCalls start error: {e}")

    # 4. Load Plugins Dynamically
    logger.info("Loading plugin modules...")
    for plugin_name in ALL_PLUGINS:
        try:
            importlib.import_module(f"StdMusic.plugins.{plugin_name}")
            logger.info(f"Plugin loaded: {plugin_name}")
        except Exception as e:
            logger.error(f"Failed to load plugin {plugin_name}: {e}", exc_info=True)

    logger.info("=" * 50)
    logger.info(f"⚡ {BOT_NAME} IS ONLINE AND STREAMING READY!")
    logger.info("=" * 50)

    # 5. Idle loop
    await idle()

    # Graceful shutdown
    logger.info("Stopping StdMusic services...")
    if pytgcalls:
        try:
            await pytgcalls.stop()
        except Exception:
            pass
    if userbot:
        try:
            await userbot.stop()
        except Exception:
            pass
    await app.stop()
    logger.info("StdMusic stopped cleanly.")


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        pass
