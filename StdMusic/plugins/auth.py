from stdgram import filters
from stdgram.types import Message

from StdMusic import app
from ..misc import is_admin, add_auth_user, remove_auth_user


@app.on_message(filters.command(["auth"]))
async def auth_user_handler(client, message: Message):
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id):
        return await message.reply_text("❌ <b>ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴀᴜᴛʜᴏʀɪᴢᴇ ᴜsᴇʀs.</b>")

    user_id = None
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1 and message.command[1].isdigit():
        user_id = int(message.command[1])

    if not user_id:
        return await message.reply_text("ℹ️ <b>ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴏʀ ᴘʀᴏᴠɪᴅᴇ ᴜsᴇʀ ɪᴅ ᴛᴏ ᴀᴜᴛʜᴏʀɪᴢᴇ.</b>")

    add_auth_user(chat_id, user_id)
    await message.reply_text(f"✅ <b>ᴜsᴇʀ {user_id} ɪs ɴᴏᴡ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ.</b>")


@app.on_message(filters.command(["unauth"]))
async def unauth_user_handler(client, message: Message):
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id):
        return await message.reply_text("❌ <b>ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ʀᴇᴠᴏᴋᴇ ᴀᴜᴛʜᴏʀɪᴢᴀᴛɪᴏɴ.</b>")

    user_id = None
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1 and message.command[1].isdigit():
        user_id = int(message.command[1])

    if not user_id:
        return await message.reply_text("ℹ️ <b>ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴏʀ ᴘʀᴏᴠɪᴅᴇ ᴜsᴇʀ ɪᴅ ᴛᴏ ʀᴇᴠᴏᴋᴇ.</b>")

    remove_auth_user(chat_id, user_id)
    await message.reply_text(f"🚫 <b>ᴜsᴇʀ {user_id} ᴀᴜᴛʜᴏʀɪᴢᴀᴛɪᴏɴ ʀᴇᴠᴏᴋᴇᴅ.</b>")
