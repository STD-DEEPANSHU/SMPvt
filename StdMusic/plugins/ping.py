import time
import psutil

from stdgram import filters
from stdgram.types import Message

from StdMusic import app, BOT_NAME
from ..utils.formatters import get_readable_time, format_bytes

START_TIME = time.time()


@app.on_message(filters.command(["ping", "status"]))
async def ping_command_handler(client, message: Message):
    start = time.time()
    msg = await message.reply_text("⚡ <b>ᴘɪɴɢɪɴɢ...</b>")
    latency = round((time.time() - start) * 1000, 2)

    uptime = get_readable_time(time.time() - START_TIME)
    ram = psutil.virtual_memory()
    ram_usage = f"{format_bytes(ram.used)} / {format_bytes(ram.total)} ({ram.percent}%)"
    cpu_usage = f"{psutil.cpu_percent()}%"

    await msg.edit_text(
        f"🏓 <b>ᴘᴏɴɢ !</b> <code>{latency} ᴍs</code>\n\n"
        f"⏱ <b>ᴜᴘᴛɪᴍᴇ :</b> <code>{uptime}</code>\n"
        f"💾 <b>ʀᴀᴍ :</b> <code>{ram_usage}</code>\n"
        f"🖥 <b>ᴄᴘᴜ :</b> <code>{cpu_usage}</code>"
    )
