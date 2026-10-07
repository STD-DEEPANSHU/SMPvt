import os
import re
import random
import aiofiles
import aiohttp
import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageFilter

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
CACHE_DIR = os.path.join(os.getcwd(), "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

BLACK_PATH = os.path.join(ASSETS_DIR, "black.jpg")
MUSIC_PNG_PATH = os.path.join(ASSETS_DIR, "music.png")
ROBOT_FONT_PATH = os.path.join(ASSETS_DIR, "robot.otf")
INFO_FONT_PATH = os.path.join(ASSETS_DIR, "iromusic.ttf")


def make_col():
    """Generate vibrant RGB accent color for player frame."""
    return (
        random.randint(60, 255),
        random.randint(60, 255),
        random.randint(60, 255),
    )


def change_image_size(max_width: int, max_height: int, image: Image.Image) -> Image.Image:
    width_ratio = max_width / image.size[0]
    height_ratio = max_height / image.size[1]
    new_width = int(width_ratio * image.size[0])
    new_height = int(height_ratio * image.size[1])
    return image.resize((new_width, new_height), Image.LANCZOS)


def truncate_title(text: str) -> list:
    words = text.split(" ")
    line1, line2 = "", ""
    for w in words:
        if len(line1) + len(w) < 27:
            line1 += " " + w
        elif len(line2) + len(w) < 25:
            line2 += " " + w
    return [line1.strip() or text[:25], line2.strip()]


async def get_thumb(
    videoid: str,
    title: str = "",
    duration: str = "",
    channel: str = "",
    views: str = "",
    thumb_url: str = "",
) -> str:
    """
    Generate high-aesthetic circular music thumbnail matching IroMusic caliber.
    Returns path to cached PNG image.
    """
    clean_id = re.sub(r"[^\w\-]", "", str(videoid))[:20] or "track"
    cache_path = os.path.join(CACHE_DIR, f"{clean_id}_iro.png")

    if os.path.isfile(cache_path) and os.path.getsize(cache_path) > 1000:
        return cache_path

    # Determine thumbnail download URL
    if not thumb_url:
        if len(clean_id) == 11:
            thumb_url = f"https://img.youtube.com/vi/{clean_id}/maxresdefault.jpg"
        else:
            thumb_url = "https://graph.org/file/bf1dae161eaca5cefdbd2.jpg"

    raw_thumb_path = os.path.join(CACHE_DIR, f"raw_{clean_id}.jpg")

    async with aiohttp.ClientSession() as session:
        downloaded = False
        try:
            async with session.get(thumb_url, timeout=10) as resp:
                if resp.status == 200:
                    async with aiofiles.open(raw_thumb_path, mode="wb") as f:
                        await f.write(await resp.read())
                    downloaded = True
        except Exception:
            pass

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
            image = Image.open(raw_thumb_path)
        else:
            image = Image.new("RGB", (1280, 720), (25, 27, 42))

        black = (
            Image.open(BLACK_PATH)
            if os.path.isfile(BLACK_PATH)
            else Image.new("RGB", (1280, 720), (10, 10, 15))
        )
        img_frame = (
            Image.open(MUSIC_PNG_PATH)
            if os.path.isfile(MUSIC_PNG_PATH)
            else Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
        )

        image5 = change_image_size(1280, 720, img_frame)
        image1 = change_image_size(1280, 720, image)
        image11 = change_image_size(1280, 720, image)

        image1 = image11.filter(ImageFilter.BoxBlur(20))
        image2 = Image.blend(image1, black, 0.6)

        im = image5.convert("RGBA")
        color = make_col()

        data = np.array(im)
        red, green, blue, alpha = data.T

        white_areas = (red == 255) & (blue == 255) & (green == 255)
        data[..., :-1][white_areas.T] = color

        im2 = Image.fromarray(data)
        image5 = im2

        # Circular crop for artwork
        image3 = image11.crop((280, 0, 1000, 720))
        lum_img = Image.new("L", [720, 720], 0)
        draw_circle = ImageDraw.Draw(lum_img)
        draw_circle.pieslice([(0, 0), (720, 720)], 0, 360, fill=255, outline="white")

        img_arr = np.array(image3)
        lum_img_arr = np.array(lum_img)
        final_img_arr = np.dstack((img_arr, lum_img_arr))
        image3 = Image.fromarray(final_img_arr)
        image3 = image3.resize((600, 600), Image.LANCZOS)

        image2.paste(image3, (50, 70), mask=image3)
        image2.paste(image5, (0, 0), mask=image5)

        # Typography
        try:
            font1 = ImageFont.truetype(ROBOT_FONT_PATH, 30)
            font2 = ImageFont.truetype(ROBOT_FONT_PATH, 60)
            font3 = ImageFont.truetype(ROBOT_FONT_PATH, 49)
            font4 = ImageFont.truetype(INFO_FONT_PATH, 35)
        except Exception:
            font1 = ImageFont.load_default()
            font2 = ImageFont.load_default()
            font3 = ImageFont.load_default()
            font4 = ImageFont.load_default()

        image4 = ImageDraw.Draw(image2)
        image4.text((10, 10), "STDMUSIC", fill="white", font=font1, align="left")
        image4.text(
            (670, 150),
            "NOW PLAYING",
            fill="white",
            font=font2,
            stroke_width=2,
            stroke_fill="white",
            align="left",
        )

        clean_title = re.sub(r"[\(\[\{].*?[\)\]\}]", "", title).strip() or title or "Now Playing Track"
        title1 = truncate_title(clean_title)
        image4.text((670, 280), text=title1[0], fill="white", font=font3, align="left")
        if title1[1]:
            image4.text((670, 332), text=title1[1], fill="white", font=font3, align="left")

        views_text = f"Views : {views}" if views else "Views : Live Stream"
        duration_text = f"Duration : {duration} minutes" if duration else "Duration : 03:45 minutes"
        channel_text = f"Channel : {channel}" if channel else "Channel : Music Hub"

        image4.text((670, 410), text=views_text, fill="white", font=font4, align="left")
        image4.text((670, 460), text=duration_text, fill="white", font=font4, align="left")
        image4.text((670, 510), text=channel_text, fill="white", font=font4, align="left")

        image2.save(cache_path, "PNG")

    finally:
        if os.path.isfile(raw_thumb_path):
            try:
                os.remove(raw_thumb_path)
            except Exception:
                pass

    return cache_path
