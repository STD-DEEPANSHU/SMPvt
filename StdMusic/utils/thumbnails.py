import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
CACHE_DIR = os.path.join(os.getcwd(), "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

FONT_PATH = os.path.join(ASSETS_DIR, "font.ttf")
FONT2_PATH = os.path.join(ASSETS_DIR, "font2.ttf")
FONT3_PATH = os.path.join(ASSETS_DIR, "font3.ttf")
PLAY_ICONS_PATH = os.path.join(ASSETS_DIR, "play_icons.png")


def _truncate_title(text: str) -> list:
    """Break title into two well-balanced lines."""
    words = text.split()
    line1, line2 = "", ""
    for w in words:
        if len(line1) + len(w) + 1 <= 28:
            line1 += (" " if line1 else "") + w
        elif len(line2) + len(w) + 1 <= 28:
            line2 += (" " if line2 else "") + w
    return [line1.strip() or text[:25], line2.strip()]


def _crop_center_circle(img: Image.Image, output_size: int = 400, border: int = 15) -> Image.Image:
    """Crop center circle with crisp white border ring."""
    min_dim = min(img.size[0], img.size[1])
    left = (img.size[0] - min_dim) // 2
    top = (img.size[1] - min_dim) // 2
    img_square = img.crop((left, top, left + min_dim, top + min_dim))
    img_square = img_square.resize((output_size - 2 * border, output_size - 2 * border), Image.LANCZOS)

    # Inner circular mask
    mask_inner = Image.new("L", (output_size - 2 * border, output_size - 2 * border), 0)
    ImageDraw.Draw(mask_inner).ellipse((0, 0, output_size - 2 * border, output_size - 2 * border), fill=255)

    final_img = Image.new("RGBA", (output_size, output_size), (255, 255, 255, 255))
    final_img.paste(img_square, (border, border), mask_inner)

    # Outer border mask
    mask_outer = Image.new("L", (output_size, output_size), 0)
    ImageDraw.Draw(mask_outer).ellipse((0, 0, output_size, output_size), fill=255)

    return Image.composite(final_img, Image.new("RGBA", (output_size, output_size), (0, 0, 0, 0)), mask_outer)


async def get_thumb(
    videoid: str,
    title: str = "",
    duration: str = "",
    channel: str = "",
    views: str = "",
    thumb_url: str = "",
) -> str:
    """
    Generate dynamic 1280x720 music thumbnail matching DaxxMusic & AnonX caliber.
    Returns path to cached PNG image.
    """
    clean_id = re.sub(r"[^\w\-]", "", str(videoid))[:20] or "track"
    cache_path = os.path.join(CACHE_DIR, f"{clean_id}_v4.png")

    if os.path.isfile(cache_path) and os.path.getsize(cache_path) > 1000:
        return cache_path

    # Determine thumbnail download URL
    if not thumb_url:
        if len(clean_id) == 11:
            thumb_url = f"https://img.youtube.com/vi/{clean_id}/maxresdefault.jpg"
        else:
            thumb_url = "https://telegra.ph/file/2034963e00fcadfb845ff.jpg"

    raw_thumb_path = os.path.join(CACHE_DIR, f"raw_{clean_id}.jpg")

    async with aiohttp.ClientSession() as session:
        # Download primary thumbnail URL
        downloaded = False
        try:
            async with session.get(thumb_url, timeout=10) as resp:
                if resp.status == 200:
                    async with aiofiles.open(raw_thumb_path, mode="wb") as f:
                        await f.write(await resp.read())
                    downloaded = True
        except Exception:
            pass

        # Fallback to hqdefault if maxresdefault 404s
        if not downloaded and len(clean_id) == 11:
            fallback_url = f"https://img.youtube.com/vi/{clean_id}/hqdefault.jpg"
            try:
                async with session.get(fallback_url, timeout=10) as resp:
                    if resp.status == 200:
                        async with aiofiles.open(raw_thumb_path, mode="wb") as f:
                            await f.write(await resp.read())
                        downloaded = True
            except Exception:
                pass

    try:
        if os.path.isfile(raw_thumb_path):
            youtube = Image.open(raw_thumb_path)
        else:
            youtube = Image.new("RGB", (1280, 720), (25, 27, 42))
    except Exception:
        youtube = Image.new("RGB", (1280, 720), (25, 27, 42))

    try:
        # 1. Background blurred and darkened
        bg = ImageOps.fit(youtube, (1280, 720)).convert("RGBA")
        bg = bg.filter(ImageFilter.BoxBlur(20))
        bg = ImageEnhance.Brightness(bg).enhance(0.55)

        # 2. Fonts
        try:
            arial = ImageFont.truetype(FONT2_PATH, 28)
            time_font = ImageFont.truetype(FONT_PATH, 28)
            title_font = ImageFont.truetype(FONT3_PATH, 42)
        except Exception:
            arial = ImageFont.load_default()
            time_font = ImageFont.load_default()
            title_font = ImageFont.load_default()

        # 3. Paste Circular Artwork
        circle_thumb = _crop_center_circle(youtube, 400, 15)
        bg.paste(circle_thumb, (120, 160), circle_thumb)

        draw = ImageDraw.Draw(bg)
        text_x = 565

        # 4. Clean text
        display_title = re.sub(r"[\(\[\{].*?[\)\]\}]", "", title).strip() or title or "Now Playing Track"
        t1, t2 = _truncate_title(display_title)
        draw.text((text_x, 180), t1, fill=(255, 255, 255), font=title_font)
        if t2:
            draw.text((text_x, 235), t2, fill=(255, 255, 255), font=title_font)

        channel_str = channel or "YouTube Stream"
        views_str = f"  |  {views}" if views else ""
        draw.text((text_x, 320), f"{channel_str[:30]}{views_str}", fill=(215, 220, 235), font=arial)

        # 5. Neon Seek Progress Bar
        line_length = 580
        played_length = int(line_length * 0.58)

        # Played track line (Vivid Crimson Neon)
        draw.line([(text_x, 380), (text_x + played_length, 380)], fill=(255, 45, 85), width=8)
        # Unplayed track line (Subtle Translucent Silver)
        draw.line([(text_x + played_length, 380), (text_x + line_length, 380)], fill=(190, 195, 205), width=8)

        # Seeker Indicator circle
        seek_x = text_x + played_length
        draw.ellipse([seek_x - 9, 380 - 9, seek_x + 9, 380 + 9], fill=(255, 45, 85))

        # Time labels
        duration_label = duration if duration else "03:45"
        draw.text((text_x, 402), "00:00", fill=(255, 255, 255), font=time_font)
        draw.text((1070, 402), duration_label, fill=(255, 255, 255), font=time_font)

        # 6. Playback controls icons
        if os.path.isfile(PLAY_ICONS_PATH):
            try:
                play_icons = Image.open(PLAY_ICONS_PATH).convert("RGBA")
                play_icons = play_icons.resize((580, 62), Image.LANCZOS)
                bg.paste(play_icons, (text_x, 450), play_icons)
            except Exception:
                pass

        # 7. Save to cache
        bg.save(cache_path, "PNG")

    finally:
        if os.path.isfile(raw_thumb_path):
            try:
                os.remove(raw_thumb_path)
            except Exception:
                pass

    return cache_path
