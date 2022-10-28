import config

from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)
from FallenMusic import BOT_USERNAME, F_OWNER


def start_pannel():
        buttons = [
            [
                InlineKeyboardButton(
                    text="ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴩ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="❄ ʜᴇʟᴩ ❄", callback_data="fallen_help"
                ),
                InlineKeyboardButton(
                    text="🥀 ᴏᴡɴᴇʀ 🥀", user_id=F_OWNER
                )
            ],
            [
                InlineKeyboardButton(
                    text="✨ sᴜᴩᴩᴏʀᴛ ✨", url=config.SUPPORT_CHAT
                ),
                InlineKeyboardButton(
                    text="💘 ᴄʜᴀɴɴᴇʟ 💘", url=config.SUPPORT_CHANNEL
                ),
            ],
            [
                InlineKeyboardButton(
                    text="☁ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ☁", url="https://gitHub.com/DevArora2604"
                )
            ],
        ]
        return buttons


def private_panel():
        buttons = [
            [
                InlineKeyboardButton(
                    text="ᴀᴅᴅ ᴍᴇ ᴇʟsᴇ ʏᴏᴜ ɢᴇʏ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🥀 ᴏᴡɴᴇʀ 🥀", user_id=F_OWNER
                ),
                InlineKeyboardButton(
                    text="❄ ʜᴇʟᴩ ❄", callback_data="fallen_help"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✨ sᴜᴩᴩᴏʀᴛ ✨", url=config.SUPPORT_CHAT
                ),
                InlineKeyboardButton(
                    text="💘 ᴄʜᴀɴɴᴇʟ 💘", url=config.SUPPORT_CHANNEL
                ),
            ],
            [
                InlineKeyboardButton(
                    text="☁ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ☁", url="https://github.com/DevArora2604"
                ),
            ],
        ]
        return buttons

