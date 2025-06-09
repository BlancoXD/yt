import requests
import os
from pathlib import Path
from uuid import uuid4

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.config import load_config

config = load_config()

ELEVENLABS_API_KEY = config["elevenlabs_api_key"]
VOICE_ID = config["voice_id"]
OUTPUT_DIR = Path("core/outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def synthesize_voice(text, filename=None):
    print(f"[ElevenLabs] Synthesizing voice for: {text[:60]}...")
    
    if not filename:
        filename = f"{uuid4().hex}.mp3"
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to synthesize: {response.status_code} {response.text}")
    
    audio_path = OUTPUT_DIR / filename
    with open(audio_path, "wb") as f:
        f.write(response.content)
    
    print(f"[ElevenLabs] Audio saved to {audio_path}")
    return str(audio_path)
