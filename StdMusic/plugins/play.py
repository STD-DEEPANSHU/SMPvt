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
from config import DURATION_LIMIT

logger = logging.getLogger("StdMusic.Play")


async def _ensure_assistant_in_chat(chat_id: int, message: Message) -> bool:
    """Ensure userbot assistant is in the target chat to join voice call."""
    if not userbot:
        await message.reply_text("❌ **Assistant userbot is not configured on this bot.**")
        return False

    try:
        ass_user = await userbot.get_me()
        try:
            await app.get_chat_member(chat_id, ass_user.id)
            return True
        except Exception:
            pass

        # Assistant not in group, attempt to join via invite link
        invite_link = await app.export_chat_invite_link(chat_id)
        await userbot.join_chat(invite_link)
        return True
    except Exception as e:
        logger.warning(f"Could not automatically add assistant to {chat_id}: {e}")
        # Allow proceed if group is public or userbot already joined
        return True


@app.on_message(filters.command(["play", "vplay", "cplay", "cvplay"]))
async def play_command_handler(client, message: Message):

    chat_id = message.chat.id
    cmd = message.command[0].lower()
    is_video = "v" in cmd

    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text(
            f"ℹ️ **Usage:**\n`/{cmd} <song name or media URL>`\n\n"
            f"Example:\n`/{cmd} Kesariya`\n`/{cmd} https://www.youtube.com/watch?v=...`"
        )

    # 1. Resolve query
    query = ""
    if len(message.command) >= 2:
        query = " ".join(message.command[1:]).strip()
    elif message.reply_to_message and (message.reply_to_message.audio or message.reply_to_message.video):
        # Media reply support
        query = message.reply_to_message.link or ""

    status_msg = await message.reply_text("⚡ *Searching track via StdAPI...*")

    try:
        # 2. Extract track info via StdAPI engine
        track = await music_engine.search(query)
        if not track or not track.get("url"):
            return await status_msg.edit_text("❌ *No matching media stream found.*")

        track["is_video"] = is_video
        track["requester"] = message.from_user.mention if message.from_user else "Admin"
        track["chat_id"] = chat_id

        title = track.get("title", "Unknown Track")
        duration = track.get("duration", 0)

        if duration and duration > DURATION_LIMIT:
            return await status_msg.edit_text(
                f"❌ **Duration limit exceeded!**\nMax allowed: {format_duration(DURATION_LIMIT)}."
            )

        # 3. Ensure assistant is ready
        if not await _ensure_assistant_in_chat(chat_id, message):
            return await status_msg.edit_text(
                "❌ **Assistant cannot access this group.** Please add the assistant manually."
            )

        # 4. Check active call status
        is_playing = await call_manager.is_active(chat_id)

        if is_playing:
            # Add to Queue
            pos = queue_manager.add(chat_id, track)
            await status_msg.edit_text(
                f"📥 **Added to Queue (#{pos})**\n\n"
                f"🎵 **Track:** `{title}`\n"
                f"⏱ **Duration:** `{format_duration(duration)}`\n"
                f"👤 **Requested by:** {track['requester']}\n\n"
                f"⚡ *Powered by [StdAPI](https://github.com/STD-DEEPANSHU/StdAPI)*",
                reply_markup=player_markup(chat_id),
            )
        else:
            # Play immediately
            await status_msg.edit_text("🚀 *Connecting to Voice Chat...*")
            await call_manager.play(chat_id, track, is_video=is_video)

            thumbnail = track.get("thumbnail")
            caption = (
                f"▶️ **Now Playing { 'Video' if is_video else 'Music' }**\n\n"
                f"🎵 **Title:** `{title}`\n"
                f"⏱ **Duration:** `{format_duration(duration)}`\n"
                f"👤 **Requested by:** {track['requester']}\n\n"
                f"⚡ *Powered by [StdGram](https://pypi.org/project/stdgram/) & [StdAPI](https://pypi.org/project/stdapi/)*"
            )

            await status_msg.delete()
            if thumbnail:
                try:
                    return await message.reply_photo(
                        photo=thumbnail,
                        caption=caption,
                        reply_markup=player_markup(chat_id),
                    )
                except Exception:
                    pass
            await message.reply_text(caption, reply_markup=player_markup(chat_id))

    except Exception as e:
        logger.error(f"Playback error in {chat_id}: {e}", exc_info=True)
        await status_msg.edit_text(f"❌ **Playback Failed:** `{e}`")
