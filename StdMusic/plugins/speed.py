import logging

try:
    from stdgram import filters
    from stdgram.types import Message
except ImportError:
    from pyrogram import filters
    from pyrogram.types import Message

from StdMusic import app
from ..core.call import call_manager
from ..misc import is_admin

logger = logging.getLogger("StdMusic.Speed")


@app.on_message(filters.command(["speed", "playback_speed", "cspeed"]))
async def speed_command_handler(client, message: Message):
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id):
        return await message.reply_text("❌ <b>ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴄʜᴀɴɢᴇ ᴘʟᴀʏʙᴀᴄᴋ sᴘᴇᴇᴅ.</b>")

    if not await call_manager.is_active(chat_id):
        return await message.reply_text("❌ <b>ɴᴏ ᴀᴄᴛɪᴠᴇ sᴛʀᴇᴀᴍ ғᴏᴜɴᴅ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.</b>")

    if len(message.command) < 2:
        return await message.reply_text(
            "ℹ️ <b>ᴘʟᴀʏʙᴀᴄᴋ sᴘᴇᴇᴅ sᴇᴛᴛɪɴɢs :</b>\n\n"
            "<b>ᴜsᴀɢᴇ :</b> <code>/speed [0.5 - 2.0]</code>\n\n"
            "<b>ᴘʀᴇsᴇᴛs :</b>\n"
            "• <code>/speed 0.75</code> (sʟᴏᴡᴇᴅ)\n"
            "• <code>/speed 1.0</code> (ɴᴏʀᴍᴀʟ)\n"
            "• <code>/speed 1.25</code> (ʙʀɪsᴋ)\n"
            "• <code>/speed 1.5</code> (ғᴀsᴛ)\n"
            "• <code>/speed 2.0</code> (2x sᴘᴇᴇᴅ)"
        )

    try:
        speed_factor = float(message.command[1])
        if speed_factor < 0.5 or speed_factor > 2.5:
            return await message.reply_text("❌ <b>sᴘᴇᴇᴅ ᴍᴜsᴛ ʙᴇ ʙᴇᴛᴡᴇᴇɴ 0.5x ᴀɴᴅ 2.5x.</b>")

        await message.reply_text(f"⚡ <b>ᴘʟᴀʏʙᴀᴄᴋ sᴘᴇᴇᴅ sᴇᴛ ᴛᴏ {speed_factor}x.</b>")
    except ValueError:
        await message.reply_text("❌ <b>ɪɴᴠᴀʟɪᴅ sᴘᴇᴇᴅ. ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴀ ᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ (ᴇ.ɢ. 1.25).</b>")
