from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from uuid import uuid4
import textwrap

OUTPUT_DIR = Path("core/outputs/thumbnails")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FONT_PATH = "arial.ttf"  # Change if you have a different font

def generate_thumbnail(title, background_color=(30, 30, 30), text_color=(255, 255, 255)):
    print(f"[Thumbnail Generator] Creating thumbnail for: {title[:50]}...")
    
    img = Image.new("RGB", (1280, 720), color=background_color)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, 60)

    wrapped_title = textwrap.fill(title, width=20)
    text_size = draw.textsize(wrapped_title, font=font)
    text_position = ((1280 - text_size[0]) // 2, (720 - text_size[1]) // 2)

    draw.text(text_position, wrapped_title, font=font, fill=text_color)

    filename = f"{uuid4().hex}_thumb.jpg"
    output_path = OUTPUT_DIR / filename
    img.save(output_path)

    print(f"[Thumbnail Generator] Saved thumbnail to {output_path}")
    return str(output_path)
