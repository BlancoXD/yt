from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from uuid import uuid4

THUMBNAIL_DIR = Path("core/outputs/thumbnails")
THUMBNAIL_DIR.mkdir(parents=True, exist_ok=True)

FONT_PATH = "arial.ttf"  # Update path if needed

def create_thumbnail_variant(text, bg_color=(0, 0, 0), text_color=(255, 255, 255)):
    print(f"[A/B Tester] Creating thumbnail with text: {text}")
    img = Image.new("RGB", (1280, 720), color=bg_color)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, 60)

    text_w, text_h = draw.textsize(text, font=font)
    position = ((1280 - text_w) // 2, (720 - text_h) // 2)
    draw.text(position, text, font=font, fill=text_color)

    filename = f"{uuid4().hex}_thumb.jpg"
    path = THUMBNAIL_DIR / filename
    img.save(path)
    print(f"[A/B Tester] Saved thumbnail to {path}")
    return str(path)

def create_multiple_variants(base_text):
    variants = []
    color_schemes = [
        ((0, 0, 0), (255, 255, 255)),
        ((255, 255, 255), (0, 0, 0)),
        ((30, 30, 30), (255, 0, 0)),
        ((255, 255, 0), (0, 0, 0))
    ]

    for bg, fg in color_schemes:
        path = create_thumbnail_variant(base_text, bg_color=bg, text_color=fg)
        variants.append(path)

    return variants
