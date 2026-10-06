import asyncio
import logging
from typing import Optional

try:
    from stdgram import filters
    from stdgram.types import Message
except ImportError:
    from pyrogram import filters
    from pyrogram.types import Message

from StdMusic import app, userbot, BOT_NAME
from ..core.engine import music_engine
from ..core.call import call_manager
from ..utils.queue import queue_manager
from ..utils.inline import player_markup, close_markup
from ..utils.formatters import format_duration
from ..utils.thumbnails import get_thumb
from config import DURATION_LIMIT

logger = logging.getLogger("StdMusic.Play")


async def _ensure_assistant_in_chat(chat_id: int, message: Message) -> bool:
    """Ensure userbot assistant is in the target chat to join voice call."""
    if not userbot:
        await message.reply_text("❌ <b>ᴀssɪsᴛᴀɴᴛ ᴜsᴇʀʙᴏᴛ ɪs ɴᴏᴛ ᴄᴏɴғɪɢᴜʀᴇᴅ.</b>")
        return False

    try:
        ass_user = await userbot.get_me()
        try:
            await app.get_chat_member(chat_id, ass_user.id)
            return True
        except Exception:
            pass

        invite_link = await app.export_chat_invite_link(chat_id)
        await userbot.join_chat(invite_link)
        return True
    except Exception as e:
        logger.warning(f"Could not automatically add assistant to {chat_id}: {e}")
        return True


@app.on_message(filters.command(["play", "vplay", "cplay", "cvplay"]))
async def play_command_handler(client, message: Message):
    chat_id = message.chat.id
    cmd = message.command[0].lower()
    is_video = "v" in cmd

    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text(
            f"ℹ️ <b>ᴜsᴀɢᴇ :</b>\n<code>/{cmd} [sᴏɴɢ ɴᴀᴍᴇ ᴏʀ ʟɪɴᴋ]</code>\n\n"
            f"<b>ᴇxᴀᴍᴘʟᴇ :</b>\n<code>/{cmd} Kesariya</code>\n<code>/{cmd} https://www.youtube.com/watch?v=...</code>"
        )

    # 1. Resolve query
    query = ""
    if len(message.command) >= 2:
        query = " ".join(message.command[1:]).strip()
    elif message.reply_to_message and (message.reply_to_message.audio or message.reply_to_message.video):
        query = message.reply_to_message.link or ""

    status_msg = await message.reply_text("🔎 <b>sᴇᴀʀᴄʜɪɴɢ...</b>")

    try:
        # 2. Extract track info via media engine
        track = await music_engine.search(query)
        if not track or not track.get("url"):
            return await status_msg.edit_text("❌ <b>ɴᴏ ʀᴇsᴜʟᴛs ғᴏᴜɴᴅ.</b>")

        track["is_video"] = is_video
        track["requester"] = message.from_user.mention if message.from_user else "Admin"
        track["chat_id"] = chat_id

        title = track.get("title", "Unknown Track")
        duration = track.get("duration", 0)
        url = track.get("url", "")
        vid_id = track.get("id", "track")
        dur_str = track.get("duration_str") or format_duration(duration)
        channel = track.get("channel", "YouTube")
        raw_thumb = track.get("thumbnail", "")

        if duration and duration > DURATION_LIMIT:
            return await status_msg.edit_text(
                f"❌ <b>ᴛʀᴀᴄᴋ ᴅᴜʀᴀᴛɪᴏɴ ᴇxᴄᴇᴇᴅs ʟɪᴍɪᴛ!</b>\nᴍᴀx ᴀʟʟᴏᴡᴇᴅ: {format_duration(DURATION_LIMIT)}."
            )

        # 3. Ensure assistant is present
        if not await _ensure_assistant_in_chat(chat_id, message):
            return await status_msg.edit_text(
                "❌ <b>ᴀssɪsᴛᴀɴᴛ ᴄᴀɴɴᴏᴛ ᴊᴏɪɴ ᴛʜɪs ᴄʜᴀᴛ.</b> ᴘʟᴇᴀsᴇ ᴀᴅᴅ ɪᴛ ᴍᴀɴᴜᴀʟʟʏ."
            )

        # 4. Generate dynamic high-res thumbnail
        thumb_path = None
        try:
            thumb_path = await get_thumb(
                videoid=vid_id,
                title=title,
                duration=dur_str,
                channel=channel,
                thumb_url=raw_thumb,
            )
        except Exception as e:
            logger.warning(f"Dynamic thumbnail generation error: {e}")
            thumb_path = raw_thumb

        # 5. Check active call status
        is_playing = await call_manager.is_active(chat_id)

        if is_playing:
            # Add to Queue
            pos = queue_manager.add(chat_id, track)
            queue_caption = (
                f"➲ <b>ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ ᴀᴛ #{pos}</b>\n\n"
                f"<b>‣ ᴛɪᴛʟᴇ :</b> <a href=\"{url}\">{title[:35]}</a>\n"
                f"<b>‣ ᴅᴜʀᴀᴛɪᴏɴ :</b> {dur_str}\n"
                f"<b>‣ ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :</b> {track['requester']}"
            )
            await status_msg.delete()
            if thumb_path:
                try:
                    return await message.reply_photo(
                        photo=thumb_path,
                        caption=queue_caption,
                        reply_markup=player_markup(chat_id),
                    )
                except Exception:
                    pass
            await message.reply_text(queue_caption, reply_markup=player_markup(chat_id))
        else:
            # Play immediately
            await status_msg.edit_text("🚀 <b>ᴊᴏɪɴɪɴɢ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ...</b>")
            await call_manager.play(chat_id, track, is_video=is_video)

            stream_caption = (
                f"➲ <b>sᴛᴀʀᴛᴇᴅ sᴛʀᴇᴀᴍɪɴɢ</b>\n\n"
                f"<b>‣ ᴛɪᴛʟᴇ :</b> <a href=\"{url}\">{title[:35]}</a>\n"
                f"<b>‣ ᴅᴜʀᴀᴛɪᴏɴ :</b> {dur_str}\n"
                f"<b>‣ ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :</b> {track['requester']}"
            )

            await status_msg.delete()
            if thumb_path:
                try:
                    return await message.reply_photo(
                        photo=thumb_path,
                        caption=stream_caption,
                        reply_markup=player_markup(chat_id),
                    )
                except Exception:
                    pass
            await message.reply_text(stream_caption, reply_markup=player_markup(chat_id))

    except Exception as e:
        logger.error(f"Playback error in {chat_id}: {e}", exc_info=True)
        await status_msg.edit_text(f"❌ <b>ᴘʟᴀʏʙᴀᴄᴋ ᴇʀʀᴏʀ :</b> <code>{e}</code>")
