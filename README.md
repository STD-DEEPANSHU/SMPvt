# StdMusic

<p align="center">
  <img src="https://telegra.ph/file/2034963e00fcadfb845ff.jpg" alt="StdMusic Banner" width="450">
</p>

<p align="center">
  <strong>Fast, sleek, and feature-rich Telegram Music & Video streaming bot.</strong><br>
  Built with high-performance voice chat streaming, dynamic album art generation, and clean inline controls.
</p>

<p align="center">
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://github.com/pytgcalls/pytgcalls"><img src="https://img.shields.io/badge/Voice%20Engine-PyTgCalls%202.3.3-00C853?style=flat-square" alt="PyTgCalls"></a>
  <a href="https://github.com/STD-DEEPANSHU/StdMusic/stargazers"><img src="https://img.shields.io/github/stars/STD-DEEPANSHU/StdMusic?style=flat-square&color=FFB300" alt="Stars"></a>
  <a href="https://github.com/STD-DEEPANSHU/StdMusic/network/members"><img src="https://img.shields.io/github/forks/STD-DEEPANSHU/StdMusic?style=flat-square&color=29B6F6" alt="Forks"></a>
  <a href="https://t.me/TeamStdNetwork"><img src="https://img.shields.io/badge/Community-TeamStdNetwork-7E57C2?style=flat-square&logo=telegram&logoColor=white" alt="Telegram"></a>
</p>

---

## Highlights

- 🎵 **Crystal Clear Audio:** 48kHz stereo stream with automatic bitrate leveling.
- 📺 **Full Video Playback:** Supports 720p/1080p video streaming directly in Telegram voice calls (`/vplay`).
- 🎨 **Dynamic Album Art:** Generates high-res 1280x720 player thumbnails on the fly with circular album cover art, blurred background, seekbar, and timestamps.
- ⚡ **Zero Playback Lag:** Instant stream resolution and seamless queue transitions.
- 🎛 **Interactive Player Controls:** Inline buttons for Pause, Resume, Skip, Stop, Shuffle, and Queue inspection.
- 🔄 **Loop & Speed Controls:** Easily loop tracks (`/loop 3`) or adjust playback speeds (`/speed 1.25`).
- 🛡 **Admin & Auth Management:** Group administrators can grant control permissions to specific users via `/auth`.

---

## Commands

### 🎵 Playback
| Command | Description |
|:---|:---|
| `/play <song / url>` | Stream high-quality audio in voice chat |
| `/vplay <video / url>` | Stream video + audio in voice chat |
| `/cplay <song / url>` | Stream audio in linked channel |
| `/cvplay <video / url>` | Stream video in linked channel |
| `/playforce <query>` | Force play immediately, skipping active stream |

### 🎛 Player Controls
| Command | Description |
|:---|:---|
| `/pause` | Pause active playback |
| `/resume` | Resume paused playback |
| `/skip` | Skip to the next track in queue |
| `/stop` or `/end` | Stop stream and leave voice chat |
| `/queue` | View current and upcoming queued tracks |
| `/loop <1-5 / off>` | Loop current track |
| `/shuffle` | Shuffle upcoming queue order |

### ⚙️ Management & Info
| Command | Description |
|:---|:---|
| `/speed <0.5 - 2.0>` | Adjust stream playback speed |
| `/auth <user>` | Authorize a non-admin to use player controls |
| `/unauth <user>` | Revoke user authorization |
| `/ping` | Check bot latency, uptime, and system status |
| `/start` | Open bot start menu and invite links |
| `/help` | Open interactive help center |

---

## Deployment

### 1. Heroku (One-Click)

Click the button below to deploy your instance to Heroku:

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/STD-DEEPANSHU/StdMusic)

---

### 2. VPS / Local Server

```bash
# Clone the repository
git clone https://github.com/STD-DEEPANSHU/StdMusic.git
cd StdMusic

# Install required dependencies
pip install -r requirements.txt

# Setup environment variables
cp sample.env .env
# Edit .env with your credentials

# Run the bot
python3 -m StdMusic
```

---

### 3. Docker

```bash
docker build -t stdmusic .
docker run -d --env-file .env --name stdmusic stdmusic
```

---

## Configuration Variables

| Variable | Description | Mandatory |
|:---|:---|:---:|
| `API_ID` | Telegram API ID from [my.telegram.org](https://my.telegram.org) | Yes |
| `API_HASH` | Telegram API Hash from [my.telegram.org](https://my.telegram.org) | Yes |
| `BOT_TOKEN` | Bot token created with [@BotFather](https://t.me/BotFather) | Yes |
| `OWNER_ID` | Your Telegram user ID | Yes |
| `SESSION_STRING` | Pyrogram / StdGram session string for assistant userbot | Yes |
| `SUDO_USERS` | Space-separated list of sudo user IDs | No |
| `DURATION_LIMIT` | Max track duration in seconds (default: `3600`) | No |
| `SUPPORT_CHAT` | Telegram support group link | No |
| `SUPPORT_CHANNEL` | Telegram updates channel link | No |

---

## Credits

- **[PyTgCalls](https://github.com/pytgcalls/pytgcalls)** for voice chat WebRTC streaming.
- **[TeamStdNetwork](https://github.com/STD-DEEPANSHU)** for maintenance and bot architecture.
- Community contributors and testers.

<p align="center">
  <sub>Maintained with ❤️ by <a href="https://github.com/STD-DEEPANSHU">STD-DEEPANSHU</a></sub>
</p>
