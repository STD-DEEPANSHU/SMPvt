try:
    from stdgram import filters
    from stdgram.types import Message, CallbackQuery
except ImportError:
    from pyrogram import filters
    from pyrogram.types import Message, CallbackQuery

from StdMusic import app, BOT_NAME, BOT_USERNAME
from ..utils.inline import start_panel, help_panel, close_markup
from config import START_IMG_URL, OWNER_ID


@app.on_message(filters.command(["start", "alive"]))
async def start_command_handler(client, message: Message):

    chat = message.chat
    bot_user = (await client.get_me()).username or BOT_USERNAME or "StdMusicBot"

    if chat.type.value == "private":
        caption = (
            f"👋 **Hey {message.from_user.mention}!**\n\n"
            f"I am **{BOT_NAME}**, a high-performance voice chat music streaming bot "
            f"powered by **[StdGram](https://pypi.org/project/stdgram/)** and "
            f"**[StdAPI](https://pypi.org/project/stdapi/)**.\n\n"
            f"✨ **Features:**\n"
            f"• 48kHz crystal clear audio streaming\n"
            f"• Zero-lag instant playback\n"
            f"• Seamless queue management & track loop\n"
            f"• High-resolution video streaming (/vplay)\n\n"
            f"Add me to your group to get started!"
        )
        if START_IMG_URL:
            try:
                return await message.reply_photo(
                    photo=START_IMG_URL,
                    caption=caption,
                    reply_markup=start_panel(bot_user),
                )
            except Exception:
                pass
        await message.reply_text(caption, reply_markup=start_panel(bot_user))
    else:
        await message.reply_text(
            f"✨ **{BOT_NAME} is active & running in {chat.title}!**\n\n"
            f"Join voice chat and send `/play <song name>` to stream music.",
            reply_markup=start_panel(bot_user),
        )


@app.on_message(filters.command(["help"]))
async def help_command_handler(client, message: Message):

    await message.reply_text(
        f"📖 **{BOT_NAME} Command Center**\n\n"
        f"Select a category below to explore available commands:",
        reply_markup=help_panel(),
    )


@app.on_callback_query(filters.regex(r"^help_"))
async def help_callback_handler(client, query: CallbackQuery):
    data = query.data
    if data == "help_play":
        text = (
            "▶️ **Playback Commands:**\n\n"
            "• `/play <song name or link>` — Stream audio in voice chat.\n"
            "• `/vplay <video name or link>` — Stream video in voice chat.\n"
            "• `/cplay <song name or link>` — Stream in linked channel.\n"
            "• `/playforce <song>` — Force play immediately interrupting queue."
        )
    elif data == "help_controls":
        text = (
            "🎛 **Player Controls:**\n\n"
            "• `/pause` — Pause current stream.\n"
            "• `/resume` — Resume paused stream.\n"
            "• `/skip` — Skip to the next song in queue.\n"
            "• `/stop` or `/end` — Stop playback and leave voice chat.\n"
            "• `/queue` — View current song and upcoming list.\n"
            "• `/loop <count>` — Loop current song (e.g. `/loop 3` or `/loop disable`).\n"
            "• `/shuffle` — Shuffle upcoming queue tracks."
        )
    elif data == "help_admin":
        text = (
            "⚙️ **Admin & Speed Commands:**\n\n"
            "• `/speed <1.0-2.0>` — Adjust playback speed.\n"
            "• `/seek <seconds>` — Seek to specific seconds in track.\n"
            "• `/auth <user_id>` — Authorize non-admin user to control player.\n"
            "• `/unauth <user_id>` — Revoke user authorization."
        )
    elif data == "help_info":
        text = (
            "ℹ️ **System & Stats:**\n\n"
            "• `/ping` — Show bot latency, uptime, and system status.\n"
            "• `/start` — Start menu and group add link."
        )
    else:  # help_back
        text = (
            f"📖 **{BOT_NAME} Command Center**\n\n"
            f"Select a category below to explore available commands:"
        )

    await query.message.edit_text(text, reply_markup=help_panel())
    await query.answer()


@app.on_callback_query(filters.regex("^close_menu$"))
async def close_menu_callback(client, query: CallbackQuery):
    try:
        await query.message.delete()
    except Exception:
        pass
