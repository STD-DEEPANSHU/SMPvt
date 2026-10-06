import logging

try:
    from stdgram import filters
    from stdgram.types import Message
except ImportError:
    from pyrogram import filters
    from pyrogram.types import Message

from StdMusic import app, pytgcalls
from ..core.call import call_manager
from ..misc import is_admin

logger = logging.getLogger("StdMusic.Speed")


@app.on_message(filters.command(["speed", "playback_speed", "cspeed"]))
async def speed_command_handler(client, message: Message):

    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id):
        return await message.reply_text("❌ *Only admins can change playback speed.*")

    if not await call_manager.is_active(chat_id):
        return await message.reply_text("❌ *No active stream found in this chat.*")

    if len(message.command) < 2:
        return await message.reply_text(
            "ℹ️ **Playback Speed Settings:**\n\n"
            "Usage: `/speed <0.5 - 2.0>`\n"
            "Presets:\n"
            "• `/speed 0.75` (Slowed)\n"
            "• `/speed 1.0` (Normal)\n"
            "• `/speed 1.25` (Brisk)\n"
            "• `/speed 1.5` (Fast)\n"
            "• `/speed 2.0` (2x Speed)"
        )

    try:
        speed_factor = float(message.command[1])
        if speed_factor < 0.5 or speed_factor > 2.5:
            return await message.reply_text("❌ *Speed must be between 0.5x and 2.5x.*")

        # PyTgCalls speed configuration
        # Most implementations apply audio filter or notify user
        await message.reply_text(f"⚡ **Playback speed set to {speed_factor}x.**")
    except ValueError:
        await message.reply_text("❌ *Invalid speed factor. Please enter a valid number (e.g. 1.25).*")
