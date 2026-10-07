import asyncio
import logging
from typing import Dict, Any, Optional

try:
    from pytgcalls.types import StreamEnded
    from pytgcalls.exceptions import NoActiveGroupCall, NotInCallError
except ImportError:
    StreamEnded = None
    NoActiveGroupCall = Exception
    NotInCallError = Exception

from StdMusic import app, userbot, pytgcalls
from .engine import music_engine
from ..utils.queue import queue_manager
from ..utils.inline import player_markup
from ..utils.thumbnails import get_thumb

logger = logging.getLogger("StdMusic.Call")

ACTIVE_CALLS: Dict[int, bool] = {}


class CallManager:
    """Manages PyTgCalls voice chat sessions, streams, and queue transitions."""

    def __init__(self):
        self.calls = pytgcalls

    async def is_active(self, chat_id: int) -> bool:
        return ACTIVE_CALLS.get(chat_id, False)

    async def play(self, chat_id: int, track: Dict[str, Any], is_video: bool = False) -> None:
        """Play track immediately in the voice chat."""
        if not self.calls:
            raise RuntimeError("Assistant userbot is not configured. Please set SESSION_STRING.")

        stream_url = await music_engine.get_stream_url(track, is_video=is_video)
        stream = music_engine.create_media_stream(stream_url, is_video=is_video)

        if await self.is_active(chat_id):
            await self.calls.change_stream(chat_id, stream)
        else:
            await self.calls.play(chat_id, stream)
            ACTIVE_CALLS[chat_id] = True

        queue_manager.set_current(chat_id, track)

    async def pause(self, chat_id: int) -> bool:
        if self.calls and await self.is_active(chat_id):
            await self.calls.pause(chat_id)
            return True
        return False

    async def resume(self, chat_id: int) -> bool:
        if self.calls and await self.is_active(chat_id):
            await self.calls.resume(chat_id)
            return True
        return False

    async def stop(self, chat_id: int) -> None:
        """Stop playback, clear queue, and leave voice chat."""
        queue_manager.clear(chat_id)
        ACTIVE_CALLS.pop(chat_id, None)
        if self.calls:
            try:
                await self.calls.leave_call(chat_id)
            except Exception as e:
                logger.debug(f"Error leaving call {chat_id}: {e}")

    async def skip(self, chat_id: int) -> Optional[Dict[str, Any]]:
        """Skip currently playing track and play next item in queue."""
        next_track = queue_manager.get_next(chat_id)
        if next_track:
            await self.play(chat_id, next_track, is_video=next_track.get("is_video", False))
            return next_track
        else:
            await self.stop(chat_id)
            return None


call_manager = CallManager()


# Register stream-end auto-advance handler
if pytgcalls:
    @pytgcalls.on_update()
    async def _on_stream_end_handler(client, update):
        if isinstance(update, StreamEnded):
            chat_id = update.chat_id
            logger.info(f"Stream ended in {chat_id}, checking queue...")
            next_track = await call_manager.skip(chat_id)
            if next_track:
                title = next_track.get("title", "Track")
                dur_str = next_track.get("duration_str", "")
                url = next_track.get("url", "")
                requester = next_track.get("requester", "Auto Queue")
                caption = (
                    f"➲ <b>sᴛᴀʀᴛᴇᴅ sᴛʀᴇᴀᴍɪɴɢ</b>\n\n"
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
                        return await app.send_photo(
                            chat_id,
                            photo=thumb_path,
                            caption=caption,
                            reply_markup=player_markup(chat_id),
                        )
                except Exception:
                    pass

                try:
                    await app.send_message(
                        chat_id,
                        caption,
                        reply_markup=player_markup(chat_id),
                    )
                except Exception:
                    pass
