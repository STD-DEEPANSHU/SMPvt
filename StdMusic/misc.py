from typing import Set
from config import SUDO_USERS, OWNER_ID

try:
    from stdgram.enums import ChatMemberStatus
except ImportError:
    from pyrogram.enums import ChatMemberStatus

from StdMusic import app

# Set of authorized non-admin users per chat
# { chat_id: set(user_id, ...) }
AUTH_USERS: dict[int, Set[int]] = {}


def is_sudo(user_id: int) -> bool:
    """Check if user is a bot owner or sudo user."""
    return user_id in SUDO_USERS or user_id == OWNER_ID


async def is_admin(chat_id: int, user_id: int) -> bool:
    """Check if user has admin rights or is sudo in the group."""
    if is_sudo(user_id):
        return True

    # Check authorized users list
    if user_id in AUTH_USERS.get(chat_id, set()):
        return True

    try:
        member = await app.get_chat_member(chat_id, user_id)
        return member.status in (ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR)
    except Exception:
        return False


def add_auth_user(chat_id: int, user_id: int) -> None:
    AUTH_USERS.setdefault(chat_id, set()).add(user_id)


def remove_auth_user(chat_id: int, user_id: int) -> None:
    if chat_id in AUTH_USERS:
        AUTH_USERS[chat_id].discard(user_id)
