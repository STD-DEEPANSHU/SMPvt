from stdgram import filters
from stdgram.types import Message, CallbackQuery

from StdMusic import app, BOT_NAME, BOT_USERNAME
from ..utils.inline import start_panel, help_panel, close_markup
from config import START_IMG_URL


@app.on_message(filters.command(["start", "alive"]))
async def start_command_handler(client, message: Message):
    chat = message.chat
    bot_user = (await client.get_me()).username or BOT_USERNAME or "StdMusicBot"

    if chat.type.value == "private":
        caption = (
            f"👋 <b>ʜᴇʏ {message.from_user.mention}!</b>\n\n"
            f"ɪ ᴀᴍ <b>{BOT_NAME}</b>, ᴀ ғᴀsᴛ ᴀɴᴅ ᴘᴏᴡᴇʀғᴜʟ ᴛᴇʟᴇɢʀᴀᴍ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ ʙᴏᴛ.\n\n"
            f"✨ <b>ғᴇᴀᴛᴜʀᴇs :</b>\n"
            f"• ᴄʀʏsᴛᴀʟ ᴄʟᴇᴀʀ 48ᴋʜᴢ ᴀᴜᴅɪᴏ sᴛʀᴇᴀᴍɪɴɢ\n"
            f"• ɪɴsᴛᴀɴᴛ ʜɪɢʜ-ᴅᴇғɪɴɪᴛɪᴏɴ ᴠɪᴅᴇᴏ sᴛʀᴇᴀᴍs (<code>/vplay</code>)\n"
            f"• ᴀᴇsᴛʜᴇᴛɪᴄ ᴅʏɴᴀᴍɪᴄ ᴛʜᴜᴍʙɴᴀɪʟ ɢᴇɴᴇʀᴀᴛɪᴏɴ\n"
            f"• ᴀᴜᴅɪᴏ ʙᴀss ʙᴏᴏsᴛ & ғɪʟᴛᴇʀs (<code>/bass</code>)\n"
            f"• ɪɴsᴛᴀɴᴛ ʏᴏᴜᴛᴜʙᴇ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ (<code>/song</code>, <code>/video</code>)\n"
            f"• sᴍᴏᴏᴛʜ ǫᴜᴇᴜᴇ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ & ʟᴏᴏᴘ ᴍᴏᴅᴇ\n"
            f"• ᴢᴇʀᴏ-ʟᴀɢ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ sʏɴᴄ\n\n"
            f"ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ!"
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
            f"✨ <b>{BOT_NAME} ɪs ᴏɴʟɪɴᴇ & ʀᴇᴀᴅʏ ɪɴ {chat.title}!</b>\n\n"
            f"ᴊᴏɪɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴀɴᴅ sᴇɴᴅ <code>/play [sᴏɴɢ]</code> ᴛᴏ sᴛᴀʀᴛ sᴛʀᴇᴀᴍɪɴɢ.",
            reply_markup=start_panel(bot_user),
        )


@app.on_message(filters.command(["help"]))
async def help_command_handler(client, message: Message):
    await message.reply_text(
        f"📖 <b>{BOT_NAME} ᴄᴏᴍᴍᴀɴᴅ ᴄᴇɴᴛᴇʀ</b>\n\n"
        f"sᴇʟᴇᴄᴛ ᴀ ᴄᴀᴛᴇɢᴏʀʏ ʙᴇʟᴏᴡ ᴛᴏ ᴇxᴘʟᴏʀᴇ ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs:",
        reply_markup=help_panel(),
    )


@app.on_callback_query(filters.regex(r"^help_"))
async def help_callback_handler(client, query: CallbackQuery):
    data = query.data
    if data == "help_play":
        text = (
            "▶️ <b>ᴘʟᴀʏʙᴀᴄᴋ ᴄᴏᴍᴍᴀɴᴅs :</b>\n\n"
            "• <code>/play [sᴏɴɢ / ᴜʀʟ]</code> — sᴛʀᴇᴀᴍ ᴀᴜᴅɪᴏ ɪɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.\n"
            "• <code>/vplay [ᴠɪᴅᴇᴏ / ᴜʀʟ]</code> — sᴛʀᴇᴀᴍ ᴠɪᴅᴇᴏ ɪɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.\n"
            "• <code>/cplay [sᴏɴɢ / ᴜʀʟ]</code> — sᴛʀᴇᴀᴍ ᴀᴜᴅɪᴏ ɪɴ ᴄʜᴀɴɴᴇʟ.\n"
            "• <code>/cvplay [ᴠɪᴅᴇᴏ / ᴜʀʟ]</code> — sᴛʀᴇᴀᴍ ᴠɪᴅᴇᴏ ɪɴ ᴄʜᴀɴɴᴇʟ.\n"
            "• <code>/playforce [sᴏɴɢ]</code> — ғᴏʀᴄᴇ ᴘʟᴀʏ ɪᴍᴍᴇᴅɪᴀᴛᴇʟʏ."
        )
    elif data == "help_controls":
        text = (
            "🎛 <b>ᴘʟᴀʏᴇʀ ᴄᴏɴᴛʀᴏʟs :</b>\n\n"
            "• <code>/pause</code> — ᴘᴀᴜsᴇ ᴄᴜʀʀᴇɴᴛ sᴛʀᴇᴀᴍ.\n"
            "• <code>/resume</code> — ʀᴇsᴜᴍᴇ ᴘᴀᴜsᴇᴅ sᴛʀᴇᴀᴍ.\n"
            "• <code>/skip</code> — sᴋɪᴘ ᴛᴏ ɴᴇxᴛ ᴛʀᴀᴄᴋ ɪɴ ǫᴜᴇᴜᴇ.\n"
            "• <code>/stop</code> ᴏʀ <code>/end</code> — sᴛᴏᴘ sᴛʀᴇᴀᴍ ᴀɴᴅ ʟᴇᴀᴠᴇ ᴠᴄ.\n"
            "• <code>/queue</code> — ᴠɪᴇᴡ ᴜᴘᴄᴏᴍɪɴɢ ᴛʀᴀᴄᴋs.\n"
            "• <code>/loop [1-5 / disable]</code> — ʟᴏᴏᴘ ᴄᴜʀʀᴇɴᴛ ᴛʀᴀᴄᴋ.\n"
            "• <code>/shuffle</code> — sʜᴜғғʟᴇ ǫᴜᴇᴜᴇ ᴛʀᴀᴄᴋs."
        )
    elif data == "help_bass":
        text = (
            "🔊 <b>ʙᴀss & ᴀᴜᴅɪᴏ ғɪʟᴛᴇʀs :</b>\n\n"
            "• <code>/bass</code> — ɪɴᴄʀᴇᴀsᴇ ᴍᴜsɪᴄ ʙᴀss (ʀᴇᴘʟʏ ᴛᴏ ᴀᴜᴅɪᴏ).\n"
            "• <code>/loudly</code> — ɪɴᴄʀᴇᴀsᴇ ᴍᴜsɪᴄ ᴠᴏʟᴜᴍᴇ (ʀᴇᴘʟʏ ᴛᴏ ᴀᴜᴅɪᴏ).\n"
            "• <code>/mono</code> — ᴄᴏɴᴠᴇʀᴛ sᴛᴇʀᴇᴏ ᴛᴏ ᴍᴏɴᴏ (ʀᴇᴘʟʏ ᴛᴏ ᴀᴜᴅɪᴏ)."
        )
    elif data == "help_download":
        text = (
            "📥 <b>ᴍᴇᴅɪᴀ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ :</b>\n\n"
            "• <code>/song [sᴏɴɢ ɴᴀᴍᴇ / ʏᴛ ʟɪɴᴋ]</code> — ᴅᴏᴡɴʟᴏᴀᴅ ᴀᴜᴅɪᴏ ᴍᴘ3.\n"
            "• <code>/video [ᴠɪᴅᴇᴏ ɴᴀᴍᴇ / ʏᴛ ʟɪɴᴋ]</code> — ᴅᴏᴡɴʟᴏᴀᴅ ᴠɪᴅᴇᴏ ᴍᴘ4."
        )
    elif data == "help_admin":
        text = (
            "⚙️ <b>ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs :</b>\n\n"
            "• <code>/speed [0.5-2.0]</code> — ᴀᴅᴊᴜsᴛ ᴘʟᴀʏʙᴀᴄᴋ sᴘᴇᴇᴅ.\n"
            "• <code>/auth [ᴜsᴇʀ]</code> — ᴀᴜᴛʜᴏʀɪᴢᴇ ᴜsᴇʀ ᴛᴏ ᴄᴏɴᴛʀᴏʟ ᴘʟᴀʏᴇʀ.\n"
            "• <code>/unauth [ᴜsᴇʀ]</code> — ʀᴇᴠᴏᴋᴇ ᴜsᴇʀ ᴀᴜᴛʜᴏʀɪᴢᴀᴛɪᴏɴ."
        )
    elif data == "help_info":
        text = (
            "ℹ️ <b>ɪɴғᴏ & sʏsᴛᴇᴍ :</b>\n\n"
            "• <code>/ping</code> — ᴄʜᴇᴄᴋ ʙᴏᴛ ʟᴀᴛᴇɴᴄʏ & sʏsᴛᴇᴍ sᴛᴀᴛs.\n"
            "• <code>/start</code> — ʙᴏᴛ sᴛᴀʀᴛ ᴍᴇɴᴜ."
        )
    else:  # help_back or help_menu
        text = (
            f"📖 <b>{BOT_NAME} ᴄᴏᴍᴍᴀɴᴅ ᴄᴇɴᴛᴇʀ</b>\n\n"
            f"sᴇʟᴇᴄᴛ ᴀ ᴄᴀᴛᴇɢᴏʀʏ ʙᴇʟᴏᴡ ᴛᴏ ᴇxᴘʟᴏʀᴇ ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs:"
        )

    try:
        await query.message.edit_text(text, reply_markup=help_panel())
    except Exception:
        pass
    await query.answer()


@app.on_callback_query(filters.regex("^close_menu$"))
async def close_menu_callback(client, query: CallbackQuery):
    try:
        await query.message.delete()
    except Exception:
        pass
