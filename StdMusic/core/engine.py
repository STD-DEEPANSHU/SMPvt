import os
import re
import asyncio
import logging
from typing import Dict, Any, Optional
try:
    from pytgcalls.types import MediaStream, AudioQuality
except ImportError:
    MediaStream = None
    AudioQuality = None


try:
    from youtube_search import YoutubeSearch
except ImportError:
    YoutubeSearch = None

try:
    import stdapi
    from stdapi import StdEngine, media
    HAS_STDAPI = True
except ImportError:
    HAS_STDAPI = False

logger = logging.getLogger("StdMusic.Engine")


class StdMusicEngine:
    """
    High-Performance Media Engine powered by StdAPI.
    Extracts high-resolution audio/video streams for Telegram Voice Chat playback.
    """

    def __init__(self):
        self.local_engine = StdEngine(use_cache=True) if HAS_STDAPI else None

    @staticmethod
    def is_url(query: str) -> bool:
        return bool(re.match(r"^https?://[^\s]+", query.strip(), re.IGNORECASE))

    async def search(self, query: str) -> Dict[str, Any]:
        """Search query and return metadata (title, url, duration, thumbnail, channel)."""
        if self.is_url(query):
            return await self.extract_from_url(query)

        # Search via YoutubeSearch or fallback query
        if YoutubeSearch:
            try:
                results = await asyncio.to_thread(YoutubeSearch, query, max_results=1)
                videos = results.videos
                if videos:
                    v = videos[0]
                    vid_id = v.get("id")
                    url = f"https://www.youtube.com/watch?v={vid_id}"
                    dur_str = v.get("duration", "0:00")
                    dur_sec = sum(int(x) * 60**i for i, x in enumerate(reversed(dur_str.split(":"))))
                    return {
                        "id": vid_id,
                        "title": v.get("title", query),
                        "url": url,
                        "duration": dur_sec,
                        "duration_str": dur_str,
                        "thumbnail": v.get("thumbnails", [""])[0] if v.get("thumbnails") else "",
                        "channel": v.get("channel", "YouTube"),
                    }
            except Exception as e:
                logger.warning(f"YoutubeSearch error: {e}")

        # Direct URL extraction fallback
        return await self.extract_from_url(query)

    async def extract_from_url(self, url: str) -> Dict[str, Any]:
        """Extract media streams and metadata using StdAPI."""
        if HAS_STDAPI:
            # 1. Try cloud / remote extraction via stdapi.media
            try:
                res = await media.download(url, format="mp3", mode="audio")
                download_url = getattr(res, "download_url", None) or res.get("download_url") or res.get("url")
                if download_url:
                    return {
                        "id": res.get("id", "media"),
                        "title": res.get("title", "Media Audio"),
                        "url": url,
                        "stream_url": download_url,
                        "duration": res.get("duration", 0),
                        "duration_str": f"{res.get('duration', 0)}s",
                        "thumbnail": res.get("thumbnail", ""),
                        "channel": res.get("author", "StdAPI"),
                    }
            except Exception as e:
                logger.warning(f"StdAPI remote extraction failed, falling back to local engine: {e}")

            # 2. Local embedded engine extraction via StdEngine (yt-dlp + stealth)
            if self.local_engine:
                try:
                    res = await self.local_engine.extract(url)
                    stream_url = res.best_audio_url or res.best_video_url
                    return {
                        "id": res.id,
                        "title": res.title,
                        "url": url,
                        "stream_url": stream_url,
                        "duration": res.duration or 0,
                        "duration_str": f"{res.duration or 0}s",
                        "thumbnail": res.thumbnail or "",
                        "channel": res.author or "StdAPI",
                    }
                except Exception as e:
                    logger.error(f"StdEngine local extraction failed: {e}")

        # Fallback dictionary if all else fails
        fallback_title = url[:30] if url else "Unknown"
        return {
            "id": "unknown",
            "title": fallback_title,
            "url": url,
            "stream_url": url,
            "duration": 0,
            "duration_str": "0:00",
            "thumbnail": "",
            "channel": "Unknown",
        }


    async def get_stream_url(self, item: Dict[str, Any]) -> str:
        """Resolve playable direct stream URL for PyTgCalls."""
        if item.get("stream_url"):
            return item["stream_url"]

        url = item.get("url", "")
        if self.local_engine and url:
            try:
                res = await self.local_engine.extract(url)
                stream_url = res.best_audio_url or res.best_video_url
                if stream_url:
                    item["stream_url"] = stream_url
                    return stream_url
            except Exception as e:
                logger.error(f"Stream resolution error: {e}")

        return url

    def create_media_stream(self, stream_path_or_url: str, is_video: bool = False) -> MediaStream:
        """Generate PyTgCalls 2.x MediaStream object."""
        if is_video:
            return MediaStream(stream_path_or_url, audio_parameters=AudioQuality.HIGH)
        return MediaStream(
            stream_path_or_url,
            audio_parameters=AudioQuality.HIGH,
            video_flags=MediaStream.Flags.IGNORE,
        )


music_engine = StdMusicEngine()
