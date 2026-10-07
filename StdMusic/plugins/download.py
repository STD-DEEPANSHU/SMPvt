import os
import re
import asyncio
import logging
import aiohttp
import aiofiles
import yt_dlp

from stdgram import filters
from stdgram.types import Message

from StdMusic import app
from ..core.engine import music_engine
from ..utils.formatters import format_duration

logger = logging.getLogger("StdMusic.Download")
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@app.on_message(filters.command(["song", "music"]))
async def song_download_handler(client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text("ℹ️ <b>ᴜsᴀɢᴇ :</b> <code>/song [sᴏɴɢ ɴᴀᴍᴇ ᴏʀ ʏᴛ ʟɪɴᴋ]</code>")

    query = " ".join(message.command[1:]).strip()
    status_msg = await message.reply_text("🔎 <b>sᴇᴀʀᴄʜɪɴɢ...</b>")

    try:
        track = await music_engine.search(query)
        if not track or not track.get("url"):
            return await status_msg.edit_text("❌ <b>ɴᴏ ʀᴇsᴜʟᴛs ғᴏᴜɴᴅ.</b>")

        title = track.get("title", "Track")
        url = track.get("url", "")
        duration = track.get("duration", 0)
        dur_str = track.get("duration_str") or format_duration(duration)
        channel = track.get("channel", "Music")
        thumb_url = track.get("thumbnail", "")

        await status_msg.edit_text("📥 <b>ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴀᴜᴅɪᴏ...</b>")

        clean_id = re.sub(r"[^\w\-]", "", str(track.get("id", "audio")))[:20]
        out_file = os.path.join(DOWNLOAD_DIR, f"{clean_id}.mp3")

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(DOWNLOAD_DIR, f"{clean_id}.%(ext)s"),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "quiet": True,
            "no_warnings": True,
            "geo_bypass": True,
        }

        def _download_task():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        await asyncio.to_thread(_download_task)

        if not os.path.isfile(out_file):
            # Fallback search if ext differed
            candidates = [
                os.path.join(DOWNLOAD_DIR, f)
                for f in os.listdir(DOWNLOAD_DIR)
                if f.startswith(clean_id)
            ]
            if candidates:
                out_file = candidates[0]

        await status_msg.edit_text("📤 <b>ᴜᴘʟᴏᴀᴅɪɴɢ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ...</b>")

        caption = (
            f"<b>‣ ᴛɪᴛʟᴇ :</b> <a href=\"{url}\">{title}</a>\n"
            f"<b>‣ ᴅᴜʀᴀᴛɪᴏɴ :</b> {dur_str}\n"
            f"<b>‣ ᴄʜᴀɴɴᴇʟ :</b> {channel}\n"
            f"<b>‣ ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :</b> {message.from_user.mention}"
        )

        thumb_file = None
        if thumb_url:
            try:
                thumb_file = os.path.join(DOWNLOAD_DIR, f"{clean_id}_thumb.jpg")
                async with aiohttp.ClientSession() as session:
                    async with session.get(thumb_url) as resp:
                        if resp.status == 200:
                            async with aiofiles.open(thumb_file, "wb") as f:
                                await f.write(await resp.read())
            except Exception:
                thumb_file = None

        await message.reply_audio(
            audio=out_file,
            title=title,
            performer=channel,
            duration=duration,
            caption=caption,
            thumb=thumb_file if thumb_file and os.path.isfile(thumb_file) else None,
        )
        await status_msg.delete()

    except Exception as e:
        logger.error(f"Song download error: {e}", exc_info=True)
        await status_msg.edit_text(f"❌ <b>ᴇʀʀᴏʀ :</b> <code>{e}</code>")

    finally:
        for f in [out_file, thumb_file]:
            if f and os.path.isfile(f):
                try:
                    os.remove(f)
                except Exception:
                    pass


@app.on_message(filters.command(["video", "vdownload"]))
async def video_download_handler(client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text("ℹ️ <b>ᴜsᴀɢᴇ :</b> <code>/video [ᴠɪᴅᴇᴏ ɴᴀᴍᴇ ᴏʀ ʏᴛ ʟɪɴᴋ]</code>")

    query = " ".join(message.command[1:]).strip()
    status_msg = await message.reply_text("🔎 <b>sᴇᴀʀᴄʜɪɴɢ...</b>")

    try:
        track = await music_engine.search(query)
        if not track or not track.get("url"):
            return await status_msg.edit_text("❌ <b>ɴᴏ ʀᴇsᴜʟᴛs ғᴏᴜɴᴅ.</b>")

        title = track.get("title", "Video")
        url = track.get("url", "")
        duration = track.get("duration", 0)
        dur_str = track.get("duration_str") or format_duration(duration)
        channel = track.get("channel", "YouTube")

        await status_msg.edit_text("📥 <b>ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴠɪᴅᴇᴏ...</b>")

        clean_id = re.sub(r"[^\w\-]", "", str(track.get("id", "video")))[:20]
        out_file = os.path.join(DOWNLOAD_DIR, f"{clean_id}.mp4")

        ydl_opts = {
            "format": "best[ext=mp4]/best",
            "outtmpl": out_file,
            "quiet": True,
            "no_warnings": True,
            "geo_bypass": True,
        }

        def _download_task():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        await asyncio.to_thread(_download_task)

        await status_msg.edit_text("📤 <b>ᴜᴘʟᴏᴀᴅɪɴɢ ᴠɪᴅᴇᴏ...</b>")

        caption = (
            f"<b>‣ ᴛɪᴛʟᴇ :</b> <a href=\"{url}\">{title}</a>\n"
            f"<b>‣ ᴅᴜʀᴀᴛɪᴏɴ :</b> {dur_str}\n"
            f"<b>‣ ᴄʜᴀɴɴᴇʟ :</b> {channel}\n"
            f"<b>‣ ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :</b> {message.from_user.mention}"
        )

        await message.reply_video(
            video=out_file,
            duration=duration,
            caption=caption,
        )
        await status_msg.delete()

    except Exception as e:
        logger.error(f"Video download error: {e}", exc_info=True)
        await status_msg.edit_text(f"❌ <b>ᴇʀʀᴏʀ :</b> <code>{e}</code>")

    finally:
        if os.path.isfile(out_file):
            try:
                os.remove(out_file)
            except Exception:
                pass
