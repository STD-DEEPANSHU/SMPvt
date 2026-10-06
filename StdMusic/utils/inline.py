try:
    from stdgram.types import InlineKeyboardMarkup, InlineKeyboardButton
except ImportError:
    from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import SUPPORT_CHAT, SUPPORT_CHANNEL, BOT_NAME


def start_panel(bot_username: str) -> InlineKeyboardMarkup:
    """Start menu inline keyboard."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="➕ Add Me to Your Group",
                    url=f"https://t.me/{bot_username}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(text="📖 Commands Help", callback_data="help_menu"),
                InlineKeyboardButton(text="📢 Channel", url=SUPPORT_CHANNEL),
            ],
            [
                InlineKeyboardButton(text="💬 Support Chat", url=SUPPORT_CHAT),
                InlineKeyboardButton(text="🌐 GitHub", url="https://github.com/STD-DEEPANSHU/StdMusic"),
            ],
        ]
    )


def player_markup(chat_id: int) -> InlineKeyboardMarkup:
    """Stream playback controller buttons."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="⏸ Pause", callback_data=f"ctrl_pause_{chat_id}"),
                InlineKeyboardButton(text="▶️ Resume", callback_data=f"ctrl_resume_{chat_id}"),
                InlineKeyboardButton(text="⏭ Skip", callback_data=f"ctrl_skip_{chat_id}"),
            ],
            [
                InlineKeyboardButton(text="⏹ Stop", callback_data=f"ctrl_stop_{chat_id}"),
                InlineKeyboardButton(text="📜 Queue", callback_data=f"ctrl_queue_{chat_id}"),
                InlineKeyboardButton(text="🔀 Shuffle", callback_data=f"ctrl_shuffle_{chat_id}"),
            ],
            [
                InlineKeyboardButton(text="🗑 Close Player", callback_data="close_menu"),
            ],
        ]
    )


def help_panel() -> InlineKeyboardMarkup:
    """Interactive help menu."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="▶️ Play Commands", callback_data="help_play"),
                InlineKeyboardButton(text="🎛 Player Controls", callback_data="help_controls"),
            ],
            [
                InlineKeyboardButton(text="⚙️ Admin & Speed", callback_data="help_admin"),
                InlineKeyboardButton(text="ℹ️ Info & Ping", callback_data="help_info"),
            ],
            [
                InlineKeyboardButton(text="🔙 Back", callback_data="help_back"),
                InlineKeyboardButton(text="🗑 Close", callback_data="close_menu"),
            ],
        ]
    )


def close_markup() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton(text="🗑 Close", callback_data="close_menu")]])
