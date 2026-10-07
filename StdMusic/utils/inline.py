from stdgram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import SUPPORT_CHAT, SUPPORT_CHANNEL


def start_panel(bot_username: str) -> InlineKeyboardMarkup:
    """Start menu inline keyboard."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕",
                    url=f"https://t.me/{bot_username}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(text="📖 ᴄᴏᴍᴍᴀɴᴅs", callback_data="help_menu"),
                InlineKeyboardButton(text="📢 ᴄʜᴀɴɴᴇʟ", url=SUPPORT_CHANNEL),
            ],
            [
                InlineKeyboardButton(text="💬 sᴜᴘᴘᴏʀᴛ", url=SUPPORT_CHAT),
                InlineKeyboardButton(text="🌐 sᴏᴜʀᴄᴇ", url="https://github.com/STD-DEEPANSHU/StdMusic"),
            ],
        ]
    )


def player_markup(chat_id: int) -> InlineKeyboardMarkup:
    """Stream playback controller buttons in sleek styling."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="▷", callback_data=f"ctrl_resume_{chat_id}"),
                InlineKeyboardButton(text="II", callback_data=f"ctrl_pause_{chat_id}"),
                InlineKeyboardButton(text="‣‣I", callback_data=f"ctrl_skip_{chat_id}"),
                InlineKeyboardButton(text="▢", callback_data=f"ctrl_stop_{chat_id}"),
            ],
            [
                InlineKeyboardButton(text="🔀 sʜᴜғғʟᴇ", callback_data=f"ctrl_shuffle_{chat_id}"),
                InlineKeyboardButton(text="📜 ǫᴜᴇᴜᴇ", callback_data=f"ctrl_queue_{chat_id}"),
            ],
            [
                InlineKeyboardButton(text="🗑 ᴄʟᴏsᴇ", callback_data="close_menu"),
            ],
        ]
    )


def help_panel() -> InlineKeyboardMarkup:
    """Interactive help menu."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="▶️ ᴘʟᴀʏʙᴀᴄᴋ", callback_data="help_play"),
                InlineKeyboardButton(text="🎛 ᴄᴏɴᴛʀᴏʟs", callback_data="help_controls"),
            ],
            [
                InlineKeyboardButton(text="🔊 ʙᴀss & ғɪʟᴛᴇʀs", callback_data="help_bass"),
                InlineKeyboardButton(text="📥 ᴅᴏᴡɴʟᴏᴀᴅs", callback_data="help_download"),
            ],
            [
                InlineKeyboardButton(text="⚙️ ᴀᴅᴍɪɴ & sᴘᴇᴇᴅ", callback_data="help_admin"),
                InlineKeyboardButton(text="ℹ️ sʏsᴛᴇᴍ & ɪɴғᴏ", callback_data="help_info"),
            ],
            [
                InlineKeyboardButton(text="🔙 ʙᴀᴄᴋ", callback_data="help_back"),
                InlineKeyboardButton(text="🗑 ᴄʟᴏsᴇ", callback_data="close_menu"),
            ],
        ]
    )


def close_markup() -> InlineKeyboardMarkup:
    """Close button markup."""
    return InlineKeyboardMarkup([[InlineKeyboardButton(text="🗑 ᴄʟᴏsᴇ", callback_data="close_menu")]])
