import json
import moviepy
import requests
import textwrap
from pathlib import Path
from uuid import uuid4
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, concatenate_videoclips, CompositeVideoClip, AudioFileClip

# Load OpenAI key
with open("config.json", "r") as f:
    config = json.load(f)

OUTPUT_DIR = Path("core/outputs/videos")
FRAME_DIR = Path("core/outputs/frames")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FRAME_DIR.mkdir(parents=True, exist_ok=True)

openai_key = config["openai_api_key"]

def generate_image(prompt, index):
    print(f"[ImageGen] Generating image for: {prompt[:60]}...")
    headers = {
        "Authorization": f"Bearer {openai_key}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }
    response = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=data)
    image_url = response.json()['data'][0]['url']

    image_path = FRAME_DIR / f"img_{index}.png"
    img = Image.open(requests.get(image_url, stream=True).raw)
    img.save(image_path)
    return str(image_path)

def add_subtitle(image_path, text):
    img = Image.open(image_path).convert("RGBA")
    txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)
    font = ImageFont.truetype("arial.ttf", 36)

    wrapped = textwrap.fill(text, width=40)
    text_w, text_h = draw.textsize(wrapped, font=font)
    position = ((img.width - text_w) // 2, img.height - text_h - 40)

    draw.text(position, wrapped, font=font, fill=(255, 255, 255, 255))
    combined = Image.alpha_composite(img, txt_layer)
    subtitled_path = image_path.replace(".png", "_subtitled.png")
    combined.convert("RGB").save(subtitled_path)
    return subtitled_path

def create_video(script, audio_path, output_filename=None):
    print("[VideoGen] Creating video...")
    sentences = [s.strip() for s in script.split('.') if s.strip()]
    clips = []

    audio = AudioFileClip(audio_path)
    duration_per_clip = audio.duration / len(sentences)

    for idx, sentence in enumerate(sentences):
        image_path = generate_image(sentence, idx)
        subtitled_image = add_subtitle(image_path, sentence)
        clip = ImageClip(subtitled_image).set_duration(duration_per_clip)
        clips.append(clip)

    final = concatenate_videoclips(clips, method="compose").set_audio(audio)

    if not output_filename:
        output_filename = f"{uuid4().hex}.mp4"

    output_path = OUTPUT_DIR / output_filename
    final.write_videofile(str(output_path), fps=24)
    print(f"[VideoGen] Video saved to {output_path}")
    return str(output_path)
