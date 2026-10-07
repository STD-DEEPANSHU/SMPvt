import os
import asyncio
import logging

from stdgram import filters
from stdgram.types import Message

from StdMusic import app

logger = logging.getLogger("StdMusic.Bass")
TEMP_DIR = os.path.join(os.getcwd(), "downloads")
os.makedirs(TEMP_DIR, exist_ok=True)


async def _process_ffmpeg(in_file: str, out_file: str, filter_args: list) -> bool:
    cmd = ["ffmpeg", "-y", "-i", in_file] + filter_args + [out_file]
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL,
    )
    await proc.wait()
    return proc.returncode == 0 and os.path.isfile(out_file) and os.path.getsize(out_file) > 100


@app.on_message(filters.command(["bass"]))
async def bass_boost_handler(client, message: Message):
    reply = message.reply_to_message
    if not reply or not (reply.audio or reply.voice):
        return await message.reply_text("❌ <b>ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀɴ ᴀᴜᴅɪᴏ ᴏʀ ᴠᴏɪᴄᴇ ᴍᴇssᴀɢᴇ.</b>")

    status = await message.reply_text("⏳ <b>ᴀᴅᴅɪɴɢ ʙᴀss ʙᴏᴏsᴛ...</b>")
    input_file = await reply.download(file_name=os.path.join(TEMP_DIR, f"bass_in_{reply.id}.mp3"))
    output_file = os.path.join(TEMP_DIR, f"bass_out_{reply.id}.mp3")

    try:
        success = await _process_ffmpeg(
            input_file,
            output_file,
            ["-af", "bass=g=11:f=110,volume=2dB"],
        )
        if not success:
            return await status.edit_text("❌ <b>ғᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ᴀᴜᴅɪᴏ.</b>")

        await status.edit_text("📤 <b>ᴜᴘʟᴏᴀᴅɪɴɢ ʙᴀss-ʙᴏᴏsᴛᴇᴅ ᴀᴜᴅɪᴏ...</b>")
        title = (reply.audio.title if reply.audio else "Audio") or "Bass Boosted"
        await message.reply_audio(
            audio=output_file,
            title=f"{title} [Bass Boosted]",
            caption=f"🔊 <b>ʙᴀss ʙᴏᴏsᴛᴇᴅ ᴀᴜᴅɪᴏ</b>\n<b>ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :</b> {message.from_user.mention}",
        )
        await status.delete()
    except Exception as e:
        logger.error(f"Bass filter error: {e}", exc_info=True)
        await status.edit_text(f"❌ <b>ᴇʀʀᴏʀ :</b> <code>{e}</code>")
    finally:
        for f in [input_file, output_file]:
            if f and os.path.isfile(f):
                try:
                    os.remove(f)
                except Exception:
                    pass


@app.on_message(filters.command(["loudly", "boost"]))
async def volume_boost_handler(client, message: Message):
    reply = message.reply_to_message
    if not reply or not (reply.audio or reply.voice):
        return await message.reply_text("❌ <b>ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀɴ ᴀᴜᴅɪᴏ ᴏʀ ᴠᴏɪᴄᴇ ᴍᴇssᴀɢᴇ.</b>")

    status = await message.reply_text("⏳ <b>ɪɴᴄʀᴇᴀsɪɴɢ ᴠᴏʟᴜᴍᴇ...</b>")
    input_file = await reply.download(file_name=os.path.join(TEMP_DIR, f"loud_in_{reply.id}.mp3"))
    output_file = os.path.join(TEMP_DIR, f"loud_out_{reply.id}.mp3")

    try:
        success = await _process_ffmpeg(
            input_file,
            output_file,
            ["-af", "volume=8dB"],
        )
        if not success:
            return await status.edit_text("❌ <b>ғᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ᴀᴜᴅɪᴏ.</b>")

        await status.edit_text("📤 <b>ᴜᴘʟᴏᴀᴅɪɴɢ ʟᴏᴜᴅᴇʀ ᴀᴜᴅɪᴏ...</b>")
        title = (reply.audio.title if reply.audio else "Audio") or "Volume Boosted"
        await message.reply_audio(
            audio=output_file,
            title=f"{title} [Louder]",
            caption=f"📢 <b>ᴠᴏʟᴜᴍᴇ ʙᴏᴏsᴛᴇᴅ ᴀᴜᴅɪᴏ</b>\n<b>ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :</b> {message.from_user.mention}",
        )
        await status.delete()
    except Exception as e:
        logger.error(f"Volume filter error: {e}", exc_info=True)
        await status.edit_text(f"❌ <b>ᴇʀʀᴏʀ :</b> <code>{e}</code>")
    finally:
        for f in [input_file, output_file]:
            if f and os.path.isfile(f):
                try:
                    os.remove(f)
                except Exception:
                    pass


@app.on_message(filters.command(["mono"]))
async def mono_handler(client, message: Message):
    reply = message.reply_to_message
    if not reply or not (reply.audio or reply.voice):
        return await message.reply_text("❌ <b>ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀɴ ᴀᴜᴅɪᴏ ᴏʀ ᴠᴏɪᴄᴇ ᴍᴇssᴀɢᴇ.</b>")

    status = await message.reply_text("⏳ <b>ᴄᴏɴᴠᴇʀᴛɪɴɢ ᴛᴏ ᴍᴏɴᴏ...</b>")
    input_file = await reply.download(file_name=os.path.join(TEMP_DIR, f"mono_in_{reply.id}.mp3"))
    output_file = os.path.join(TEMP_DIR, f"mono_out_{reply.id}.mp3")

    try:
        success = await _process_ffmpeg(
            input_file,
            output_file,
            ["-ac", "1"],
        )
        if not success:
            return await status.edit_text("❌ <b>ғᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ᴀᴜᴅɪᴏ.</b>")

        await status.edit_text("📤 <b>ᴜᴘʟᴏᴀᴅɪɴɢ ᴍᴏɴᴏ ᴀᴜᴅɪᴏ...</b>")
        title = (reply.audio.title if reply.audio else "Audio") or "Mono Audio"
        await message.reply_audio(
            audio=output_file,
            title=f"{title} [Mono]",
            caption=f"🎧 <b>ᴍᴏɴᴏ ᴀᴜᴅɪᴏ</b>\n<b>ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :</b> {message.from_user.mention}",
        )
        await status.delete()
    except Exception as e:
        logger.error(f"Mono filter error: {e}", exc_info=True)
        await status.edit_text(f"❌ <b>ᴇʀʀᴏʀ :</b> <code>{e}</code>")
    finally:
        for f in [input_file, output_file]:
            if f and os.path.isfile(f):
                try:
                    os.remove(f)
                except Exception:
                    pass
