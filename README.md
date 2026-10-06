# StdMusic

<p align="center">
  <strong>High-Performance Telegram Voice Chat Music Bot</strong><br>
  <em>Engineered with StdGram, PyTgCalls 2.3.3, and the StdAPI Media Engine.</em>
</p>

<p align="center">
  <a href="https://pypi.org/project/stdgram/"><img src="https://img.shields.io/badge/Framework-StdGram-blue?style=flat-square" alt="StdGram"></a>
  <a href="https://pypi.org/project/stdapi/"><img src="https://img.shields.io/badge/Media%20Engine-StdAPI-orange?style=flat-square" alt="StdAPI"></a>
  <a href="https://github.com/pytgcalls/pytgcalls"><img src="https://img.shields.io/badge/Voice-PyTgCalls%202.3.3-green?style=flat-square" alt="PyTgCalls"></a>
  <a href="https://github.com/STD-DEEPANSHU/StdMusic"><img src="https://img.shields.io/github/stars/STD-DEEPANSHU/StdMusic?style=flat-square" alt="Stars"></a>
  <a href="https://t.me/TeamStdNetwork"><img src="https://img.shields.io/badge/Support-TeamStdNetwork-blueviolet?style=flat-square" alt="Support"></a>
</p>

---

## Overview

**StdMusic** is an ultra-fast, modern Telegram music streaming bot designed to play high-fidelity audio and video streams in group voice chats and channels.

Unlike legacy music bots that rely on fragile third-party scrapers or outdated libraries, StdMusic is powered by:
- **[StdGram](https://pypi.org/project/stdgram/):** Next-generation Telegram MTProto client with automatic FloodWait recovery and zero dispatcher freezes.
- **[StdAPI](https://pypi.org/project/stdapi/):** Universal media extraction engine providing instant stream resolution without downtime.
- **[PyTgCalls 2.3.3](https://github.com/pytgcalls/pytgcalls):** Modern WebRTC voice chat streaming engine with 48kHz audio clarity and hardware-accelerated video rendering.

---

## Features

- 🎵 **Instant Audio & Video Streaming:** Play any YouTube track, direct media URL, or query in seconds.
- 📺 **Full Video Streaming Support:** `/vplay` command for seamless group video watch parties.
- 📜 **In-Memory Queue Engine:** Zero-latency track transitions and loop playback (`/loop`).
- 🎛 **Interactive Player Controls:** Clean inline buttons for Pause, Resume, Skip, Stop, and Queue inspection.
- ⚡ **Zero Dispatcher Freezes:** Built directly on StdGram to eliminate floodwait blocks in active groups.
- 🔒 **Admin & Authorization Management:** Group admins can authorize specific users (`/auth`) to control the player.
- 🎚 **Playback Speed Control:** Adjust playback speed on the fly (`/speed 1.25x`, `1.5x`, `2.0x`).

---

## Commands

### 🎵 Playback Commands
| Command | Description |
|:---|:---|
| `/play <query or link>` | Streams high-quality audio in voice chat. |
| `/vplay <query or link>` | Streams video + audio in voice chat. |
| `/cplay <query or link>` | Streams audio in linked channel. |
| `/cvplay <query or link>` | Streams video in linked channel. |

### 🎛 Player Controls
| Command | Description |
|:---|:---|
| `/pause` | Pauses currently playing stream. |
| `/resume` | Resumes paused stream. |
| `/skip` | Skips to the next track in queue. |
| `/stop` or `/end` | Stops playback, clears queue, and leaves voice chat. |
| `/queue` | Displays currently playing track and upcoming queue. |
| `/loop <1-5 or disable>` | Loops the current track. |
| `/shuffle` | Shuffles upcoming tracks in queue. |

### ⚙️ Admin & Utilities
| Command | Description |
|:---|:---|
| `/speed <0.5 - 2.0>` | Changes playback speed. |
| `/auth <user_id>` | Authorizes a non-admin to use player controls. |
| `/unauth <user_id>` | Revokes user authorization. |
| `/ping` | Displays latency, uptime, RAM, and CPU usage. |
| `/start` | Displays start menu and group add link. |
| `/help` | Interactive command center. |

---

## Deployment Guide

### 1. Local / VPS Deployment

```bash
# 1. Clone repository
git clone https://github.com/STD-DEEPANSHU/StdMusic.git
cd StdMusic

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp sample.env .env
# Edit .env with your API_ID, API_HASH, BOT_TOKEN, and SESSION_STRING

# 4. Start the bot
python3 -m StdMusic
```

### 2. Docker Deployment

```bash
docker build -t stdmusic .
docker run -d --env-file .env --name stdmusic stdmusic
```

### 3. Heroku (1-Click)

Click the button below to deploy your own instance of StdMusic on Heroku:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/STD-DEEPANSHU/StdMusic)

---

## Required Environment Variables

| Variable | Description |
|:---|:---|
| `API_ID` | Telegram API ID from [my.telegram.org](https://my.telegram.org). |
| `API_HASH` | Telegram API Hash from [my.telegram.org](https://my.telegram.org). |
| `BOT_TOKEN` | Telegram Bot Token from [@BotFather](https://t.me/BotFather). |
| `OWNER_ID` | Telegram user ID of the Bot Owner. |
| `SESSION_STRING` | Pyrogram / StdGram session string for the assistant userbot. |
| `SUDO_USERS` | Space-separated Telegram user IDs of trusted admins. |
| `DURATION_LIMIT` | Maximum allowed song duration in seconds (default: `3600`). |

---

## Credits & Upstream Acknowledgements

- **[PyTgCalls](https://github.com/pytgcalls/pytgcalls)** — High-performance Telegram voice chat WebRTC client.
- **[StdGram](https://pypi.org/project/stdgram/)** — Next-Gen MTProto framework with native auto-recovery.
- **[StdAPI](https://pypi.org/project/stdapi/)** — Universal media extraction engine.
- **TeamStdNetwork** — Architecture, maintenance, and development.

```
Maintained by STD-DEEPANSHU <stddeepanshu@aol.com>
TeamStdNetwork (https://github.com/STD-DEEPANSHU)
```
