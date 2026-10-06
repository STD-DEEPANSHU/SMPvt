import logging

try:
    from stdgram import filters
    from stdgram.types import Message, CallbackQuery
except ImportError:
    from pyrogram import filters
    from pyrogram.types import Message, CallbackQuery

from StdMusic import app
from ..core.call import call_manager
from ..utils.queue import queue_manager
from ..utils.inline import player_markup, close_markup
from ..utils.formatters import format_duration
from ..misc import is_admin

logger = logging.getLogger("StdMusic.Control")


@app.on_message(filters.command(["pause"]))
async def pause_command_handler(client, message: Message):
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id):
        return await message.reply_text("❌ *Only admins can control music playback.*")

    if await call_manager.pause(chat_id):
        await message.reply_text("⏸ **Playback has been paused.**")
    else:
        await message.reply_text("❌ *No active stream found to pause.*")


@app.on_message(filters.command(["resume"]))
async def resume_command_handler(client, message: Message):
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id):
        return await message.reply_text("❌ *Only admins can control music playback.*")

    if await call_manager.resume(chat_id):
        await message.reply_text("▶️ **Playback has been resumed.**")
    else:
        await message.reply_text("❌ *No paused stream found to resume.*")


@app.on_message(filters.command(["skip", "next"]))
async def skip_command_handler(client, message: Message):
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id):
        return await message.reply_text("❌ *Only admins can skip songs.*")

    next_track = await call_manager.skip(chat_id)
    if next_track:
        title = next_track.get("title", "Track")
        await message.reply_text(
            f"⏭ **Skipped! Now playing:**\n`{title}`",
            reply_markup=player_markup(chat_id),
        )
    else:
        await message.reply_text("⏹ **Queue ended. Voice chat session closed.**")


@app.on_message(filters.command(["stop", "end"]))
async def stop_command_handler(client, message: Message):
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id):
        return await message.reply_text("❌ *Only admins can stop playback.*")

    await call_manager.stop(chat_id)
    await message.reply_text("⏹ **Music stopped and voice chat left.**")


@app.on_message(filters.command(["queue", "q"]))
async def queue_command_handler(client, message: Message):
    chat_id = message.chat.id
    current = queue_manager.get_current(chat_id)
    queue = queue_manager.get_queue(chat_id)

    if not current and not queue:
        return await message.reply_text("📭 **Queue is currently empty.**")

    text = "📜 **Current Stream Queue:**\n\n"
    if current:
        text += f"▶️ **Now Playing:** `{current.get('title')}` ({format_duration(current.get('duration', 0))})\n"
        text += f"👤 *Requested by:* {current.get('requester', 'Admin')}\n\n"

    if queue:
        text += "📋 **Upcoming Tracks:**\n"
        for i, t in enumerate(queue[:10], 1):
            text += f"`{i}.` `{t.get('title')[:35]}` ({format_duration(t.get('duration', 0))})\n"
        if len(queue) > 10:
            text += f"\n... and **{len(queue) - 10}** more tracks."
    else:
        text += "📋 *No more tracks in queue.*"

    await message.reply_text(text, reply_markup=close_markup())


@app.on_message(filters.command(["loop"]))
async def loop_command_handler(client, message: Message):
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id):
        return await message.reply_text("❌ *Only admins can set loop.*")

    if len(message.command) < 2:
        curr = queue_manager.get_loop(chat_id)
        return await message.reply_text(
            f"🔁 **Loop Status:** `{'Enabled (' + str(curr) + 'x)' if curr else 'Disabled'}`\n\n"
            f"Usage: `/loop 3` (loop 3 times) or `/loop disable`."
        )

    arg = message.command[1].lower()
    if arg in ("disable", "off", "0"):
        queue_manager.set_loop(chat_id, 0)
        await message.reply_text("🔁 **Track loop disabled.**")
    elif arg.isdigit():
        count = int(arg)
        queue_manager.set_loop(chat_id, count)
        await message.reply_text(f"🔁 **Loop enabled for {count} playback(s).**")
    else:
        await message.reply_text("ℹ️ *Please provide a valid loop number or 'disable'.*")


@app.on_message(filters.command(["shuffle"]))
async def shuffle_command_handler(client, message: Message):
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id):
        return await message.reply_text("❌ *Only admins can shuffle the queue.*")

    if queue_manager.shuffle(chat_id):
        await message.reply_text("🔀 **Queue has been shuffled!**")
    else:
        await message.reply_text("❌ *Queue must have at least 2 upcoming tracks to shuffle.*")


# --- Inline Callbacks for Player Controller Buttons ---
@app.on_callback_query(filters.regex(r"^ctrl_"))
async def player_callback_handler(client, query: CallbackQuery):
    data = query.data
    parts = data.split("_")
    action = parts[1]
    chat_id = int(parts[2])

    if not await is_admin(chat_id, query.from_user.id):
        return await query.answer("❌ You must be an admin to use player controls.", show_alert=True)

    if action == "pause":
        if await call_manager.pause(chat_id):
            await query.answer("⏸ Paused playback.")
        else:
            await query.answer("No active stream to pause.", show_alert=True)

    elif action == "resume":
        if await call_manager.resume(chat_id):
            await query.answer("▶️ Resumed playback.")
        else:
            await query.answer("No paused stream to resume.", show_alert=True)

    elif action == "skip":
        await query.answer("⏭ Skipping track...")
        next_track = await call_manager.skip(chat_id)
        if next_track:
            await query.message.reply_text(f"⏭ **Skipped! Now playing:**\n`{next_track.get('title')}`")
        else:
            await query.message.reply_text("⏹ **Queue ended. Voice chat closed.**")

    elif action == "stop":
        await call_manager.stop(chat_id)
        await query.answer("⏹ Music stopped.", show_alert=True)
        try:
            await query.message.delete()
        except Exception:
            pass

    elif action == "queue":
        current = queue_manager.get_current(chat_id)
        q = queue_manager.get_queue(chat_id)
        status = f"Playing: {current.get('title', 'None')[:25]} | Upcoming: {len(q)}" if current else "Queue empty"
        await query.answer(status, show_alert=True)

    elif action == "shuffle":
        if queue_manager.shuffle(chat_id):
            await query.answer("🔀 Queue shuffled!")
        else:
            await query.answer("Not enough songs in queue to shuffle.", show_alert=True)
