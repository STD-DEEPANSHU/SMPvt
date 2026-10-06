import time
import psutil
from datetime import datetime

try:
    from stdgram import filters
    from stdgram.types import Message
except ImportError:
    from pyrogram import filters
    from pyrogram.types import Message

from StdMusic import app, BOT_NAME
from ..utils.formatters import get_readable_time, format_bytes

START_TIME = time.time()


@app.on_message(filters.command(["ping", "status"]))
async def ping_command_handler(client, message: Message):

    start = time.time()
    msg = await message.reply_text("⚡ *Checking latency...*")
    latency = round((time.time() - start) * 1000, 2)

    uptime = get_readable_time(time.time() - START_TIME)
    ram = psutil.virtual_memory()
    ram_usage = f"{format_bytes(ram.used)} / {format_bytes(ram.total)} ({ram.percent}%)"
    cpu_usage = f"{psutil.cpu_percent()}%"

    await msg.edit_text(
        f"🏓 **PONG!** `{latency} ms`\n\n"
        f"🤖 **Bot:** `{BOT_NAME}`\n"
        f"⏱ **Uptime:** `{uptime}`\n"
        f"💾 **RAM Usage:** `{ram_usage}`\n"
        f"🖥 **CPU Usage:** `{cpu_usage}`\n"
        f"🚀 **Core Engine:** `StdGram + StdAPI + PyTgCalls 2.3.3`\n\n"
        f"⚡ *Maintained by [TeamStdNetwork](https://github.com/STD-DEEPANSHU)*"
    )
