import random
from typing import Dict, List, Any, Optional

# In-Memory Queue Store per Chat ID
# { chat_id: [track1, track2, ...] }
CHAT_QUEUES: Dict[int, List[Dict[str, Any]]] = {}

# Currently Playing Track Metadata per Chat ID
# { chat_id: track_metadata }
CURRENT_TRACKS: Dict[int, Dict[str, Any]] = {}

# Looping State per Chat ID (0 = disabled, >0 = remaining loop count)
LOOP_STATE: Dict[int, int] = {}


class QueueManager:
    """High-performance in-memory queue manager for Telegram voice chat playback."""

    @staticmethod
    def get_queue(chat_id: int) -> List[Dict[str, Any]]:
        return CHAT_QUEUES.setdefault(chat_id, [])

    @staticmethod
    def add(chat_id: int, track: Dict[str, Any]) -> int:
        """Add track to chat queue and return queue position."""
        q = QueueManager.get_queue(chat_id)
        q.append(track)
        return len(q)

    @staticmethod
    def get_current(chat_id: int) -> Optional[Dict[str, Any]]:
        return CURRENT_TRACKS.get(chat_id)

    @staticmethod
    def set_current(chat_id: int, track: Dict[str, Any]) -> None:
        CURRENT_TRACKS[chat_id] = track

    @staticmethod
    def get_next(chat_id: int) -> Optional[Dict[str, Any]]:
        """Get next track, honoring loop settings."""
        # 1. Check if current track is on loop
        loop_count = LOOP_STATE.get(chat_id, 0)
        current = CURRENT_TRACKS.get(chat_id)
        if loop_count > 0 and current:
            LOOP_STATE[chat_id] = loop_count - 1
            return current

        # 2. Get from queue
        q = QueueManager.get_queue(chat_id)
        if q:
            next_track = q.pop(0)
            CURRENT_TRACKS[chat_id] = next_track
            return next_track

        # 3. Queue is empty
        CURRENT_TRACKS.pop(chat_id, None)
        return None

    @staticmethod
    def clear(chat_id: int) -> None:
        CHAT_QUEUES.pop(chat_id, None)
        CURRENT_TRACKS.pop(chat_id, None)
        LOOP_STATE.pop(chat_id, None)

    @staticmethod
    def shuffle(chat_id: int) -> bool:
        q = QueueManager.get_queue(chat_id)
        if len(q) > 1:
            random.shuffle(q)
            return True
        return False

    @staticmethod
    def set_loop(chat_id: int, count: int) -> None:
        LOOP_STATE[chat_id] = count

    @staticmethod
    def get_loop(chat_id: int) -> int:
        return LOOP_STATE.get(chat_id, 0)


queue_manager = QueueManager()
