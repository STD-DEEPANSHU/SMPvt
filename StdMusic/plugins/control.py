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
from ..utils.thumbnails import get_thumb
from ..misc import is_admin

logger = logging.getLogger("StdMusic.Control")


@app.on_message(filters.command(["pause"]))
async def pause_command_handler(client, message: Message):
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id):
        return await message.reply_text("❌ <b>ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴄᴏɴᴛʀᴏʟ ᴍᴜsɪᴄ.</b>")

    if await call_manager.pause(chat_id):
        await message.reply_text("⏸ <b>sᴛʀᴇᴀᴍ ᴘᴀᴜsᴇᴅ.</b>")
    else:
        await message.reply_text("❌ <b>ɴᴏ ᴀᴄᴛɪᴠᴇ sᴛʀᴇᴀᴍ ғᴏᴜɴᴅ.</b>")


@app.on_message(filters.command(["resume"]))
async def resume_command_handler(client, message: Message):
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id):
        return await message.reply_text("❌ <b>ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴄᴏɴᴛʀᴏʟ ᴍᴜsɪᴄ.</b>")

    if await call_manager.resume(chat_id):
        await message.reply_text("▶️ <b>sᴛʀᴇᴀᴍ ʀᴇsᴜᴍᴇᴅ.</b>")
    else:
        await message.reply_text("❌ <b>ɴᴏ ᴘᴀᴜsᴇᴅ sᴛʀᴇᴀᴍ ғᴏᴜɴᴅ.</b>")


@app.on_message(filters.command(["skip", "next"]))
async def skip_command_handler(client, message: Message):
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id):
        return await message.reply_text("❌ <b>ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ sᴋɪᴘ sᴏɴɢs.</b>")

    next_track = await call_manager.skip(chat_id)
    if next_track:
        title = next_track.get("title", "Track")
        dur_str = next_track.get("duration_str", "")
        url = next_track.get("url", "")
        requester = next_track.get("requester", message.from_user.mention if message.from_user else "Admin")
        caption = (
            f"➲ <b>sᴋɪᴘᴘᴇᴅ! sᴛᴀʀᴛᴇᴅ sᴛʀᴇᴀᴍɪɴɢ</b>\n\n"
            f"<b>‣ ᴛɪᴛʟᴇ :</b> <a href=\"{url}\">{title[:35]}</a>\n"
            f"<b>‣ ᴅᴜʀᴀᴛɪᴏɴ :</b> {dur_str}\n"
            f"<b>‣ ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :</b> {requester}"
        )
        try:
            thumb_path = await get_thumb(
                videoid=next_track.get("id", "track"),
                title=title,
                duration=dur_str,
                channel=next_track.get("channel", ""),
                thumb_url=next_track.get("thumbnail", ""),
            )
            if thumb_path:
                return await message.reply_photo(
                    photo=thumb_path,
                    caption=caption,
                    reply_markup=player_markup(chat_id),
                )
        except Exception:
            pass
        await message.reply_text(caption, reply_markup=player_markup(chat_id))
    else:
        await message.reply_text("⏹ <b>ǫᴜᴇᴜᴇ ᴇɴᴅᴇᴅ. ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴄʟᴏsᴇᴅ.</b>")


@app.on_message(filters.command(["stop", "end"]))
async def stop_command_handler(client, message: Message):
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id):
        return await message.reply_text("❌ <b>ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ sᴛᴏᴘ ᴘʟᴀʏʙᴀᴄᴋ.</b>")

    await call_manager.stop(chat_id)
    await message.reply_text("⏹ <b>sᴛʀᴇᴀᴍ sᴛᴏᴘᴘᴇᴅ & ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ʟᴇғᴛ.</b>")


@app.on_message(filters.command(["queue", "q"]))
async def queue_command_handler(client, message: Message):
    chat_id = message.chat.id
    current = queue_manager.get_current(chat_id)
    queue = queue_manager.get_queue(chat_id)

    if not current and not queue:
        return await message.reply_text("📭 <b>ǫᴜᴇᴜᴇ ɪs ᴄᴜʀʀᴇɴᴛʟʏ ᴇᴍᴘᴛʏ.</b>")

    text = "📜 <b>ᴄᴜʀʀᴇɴᴛ sᴛʀᴇᴀᴍ ǫᴜᴇᴜᴇ :</b>\n\n"
    if current:
        url = current.get("url", "")
        title = current.get("title", "Track")[:35]
        text += f"▶️ <b>ɴᴏᴡ ᴘʟᴀʏɪɴɢ :</b> <a href=\"{url}\">{title}</a>\n"
        text += f"⏱ <b>ᴅᴜʀᴀᴛɪᴏɴ :</b> {current.get('duration_str') or format_duration(current.get('duration', 0))}\n"
        text += f"👤 <b>ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :</b> {current.get('requester', 'Admin')}\n\n"

    if queue:
        text += "📋 <b>ᴜᴘᴄᴏᴍɪɴɢ ᴛʀᴀᴄᴋs :</b>\n"
        for i, t in enumerate(queue[:10], 1):
            t_url = t.get("url", "")
            t_title = t.get("title", "Track")[:30]
            t_dur = t.get("duration_str") or format_duration(t.get("duration", 0))
            text += f"<b>{i}.</b> <a href=\"{t_url}\">{t_title}</a> (<code>{t_dur}</code>)\n"
        if len(queue) > 10:
            text += f"\n... ᴀɴᴅ <b>{len(queue) - 10}</b> ᴍᴏʀᴇ ᴛʀᴀᴄᴋs."
    else:
        text += "📋 <i>ɴᴏ ᴍᴏʀᴇ ᴛʀᴀᴄᴋs ɪɴ ǫᴜᴇᴜᴇ.</i>"

    await message.reply_text(text, reply_markup=close_markup(), disable_web_page_preview=True)


@app.on_message(filters.command(["loop"]))
async def loop_command_handler(client, message: Message):
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id):
        return await message.reply_text("❌ <b>ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ sᴇᴛ ʟᴏᴏᴘ.</b>")

    if len(message.command) < 2:
        curr = queue_manager.get_loop(chat_id)
        return await message.reply_text(
            f"🔁 <b>ʟᴏᴏᴘ sᴛᴀᴛᴜs :</b> <code>{'ᴇɴᴀʙʟᴇᴅ (' + str(curr) + 'x)' if curr else 'ᴅɪsᴀʙʟᴇᴅ'}</code>\n\n"
            f"<b>ᴜsᴀɢᴇ :</b> <code>/loop 3</code> ᴏʀ <code>/loop disable</code>."
        )

    arg = message.command[1].lower()
    if arg in ("disable", "off", "0"):
        queue_manager.set_loop(chat_id, 0)
        await message.reply_text("🔁 <b>ᴛʀᴀᴄᴋ ʟᴏᴏᴘ ᴅɪsᴀʙʟᴇᴅ.</b>")
    elif arg.isdigit():
        count = int(arg)
        queue_manager.set_loop(chat_id, count)
        await message.reply_text(f"🔁 <b>ʟᴏᴏᴘ ᴇɴᴀʙʟᴇᴅ ғᴏʀ {count} ᴘʟᴀʏʙᴀᴄᴋ(s).</b>")
    else:
        await message.reply_text("ℹ️ <b>ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ ᴏʀ 'disable'.</b>")


@app.on_message(filters.command(["shuffle"]))
async def shuffle_command_handler(client, message: Message):
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id):
        return await message.reply_text("❌ <b>ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ sʜᴜғғʟᴇ ᴛʜᴇ ǫᴜᴇᴜᴇ.</b>")

    if queue_manager.shuffle(chat_id):
        await message.reply_text("🔀 <b>ǫᴜᴇᴜᴇ ʜᴀs ʙᴇᴇɴ sʜᴜғғʟᴇᴅ!</b>")
    else:
        await message.reply_text("❌ <b>ᴀᴛ ʟᴇᴀsᴛ 2 ᴜᴘᴄᴏᴍɪɴɢ ᴛʀᴀᴄᴋs ɴᴇᴇᴅᴇᴅ ᴛᴏ sʜᴜғғʟᴇ.</b>")


# --- Inline Callbacks for Player Controller Buttons ---
@app.on_callback_query(filters.regex(r"^ctrl_"))
async def player_callback_handler(client, query: CallbackQuery):
    data = query.data
    parts = data.split("_")
    action = parts[1]
    chat_id = int(parts[2])

    if not await is_admin(chat_id, query.from_user.id):
        return await query.answer("❌ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴄᴏɴᴛʀᴏʟ ᴘʟᴀʏᴇʀ.", show_alert=True)

    if action == "pause":
        if await call_manager.pause(chat_id):
            await query.answer("⏸ ᴘᴀᴜsᴇᴅ.")
        else:
            await query.answer("ɴᴏ ᴀᴄᴛɪᴠᴇ sᴛʀᴇᴀᴍ ᴛᴏ ᴘᴀᴜsᴇ.", show_alert=True)

    elif action == "resume":
        if await call_manager.resume(chat_id):
            await query.answer("▶️ ʀᴇsᴜᴍᴇᴅ.")
        else:
            await query.answer("ɴᴏ ᴘᴀᴜsᴇᴅ sᴛʀᴇᴀᴍ ᴛᴏ ʀᴇsᴜᴍᴇ.", show_alert=True)

    elif action == "skip":
        await query.answer("⏭ sᴋɪᴘᴘɪɴɢ...")
        next_track = await call_manager.skip(chat_id)
        if next_track:
            title = next_track.get("title", "Track")
            dur_str = next_track.get("duration_str", "")
            url = next_track.get("url", "")
            caption = (
                f"➲ <b>sᴋɪᴘᴘᴇᴅ! sᴛᴀʀᴛᴇᴅ sᴛʀᴇᴀᴍɪɴɢ</b>\n\n"
                f"<b>‣ ᴛɪᴛʟᴇ :</b> <a href=\"{url}\">{title[:35]}</a>\n"
                f"<b>‣ ᴅᴜʀᴀᴛɪᴏɴ :</b> {dur_str}\n"
                f"<b>‣ ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :</b> {query.from_user.mention}"
            )
            try:
                thumb_path = await get_thumb(
                    videoid=next_track.get("id", "track"),
                    title=title,
                    duration=dur_str,
                    channel=next_track.get("channel", ""),
                    thumb_url=next_track.get("thumbnail", ""),
                )
                if thumb_path:
                    return await query.message.reply_photo(
                        photo=thumb_path,
                        caption=caption,
                        reply_markup=player_markup(chat_id),
                    )
            except Exception:
                pass
            await query.message.reply_text(caption, reply_markup=player_markup(chat_id))
        else:
            await query.message.reply_text("⏹ <b>ǫᴜᴇᴜᴇ ᴇɴᴅᴇᴅ. ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴄʟᴏsᴇᴅ.</b>")

    elif action == "stop":
        await call_manager.stop(chat_id)
        await query.answer("⏹ sᴛʀᴇᴀᴍ sᴛᴏᴘᴘᴇᴅ.", show_alert=True)
        try:
            await query.message.delete()
        except Exception:
            pass

    elif action == "queue":
        current = queue_manager.get_current(chat_id)
        q = queue_manager.get_queue(chat_id)
        status = f"Playing: {current.get('title', 'None')[:25]} | Queue: {len(q)}" if current else "Queue empty"
        await query.answer(status, show_alert=True)

    elif action == "shuffle":
        if queue_manager.shuffle(chat_id):
            await query.answer("🔀 ǫᴜᴇᴜᴇ sʜᴜғғʟᴇᴅ!")
        else:
            await query.answer("ɴᴏᴛ ᴇɴᴏᴜɢʜ sᴏɴɢs ɪɴ ǫᴜᴇᴜᴇ.", show_alert=True)
