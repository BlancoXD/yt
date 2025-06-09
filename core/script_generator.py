import openai
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.config import load_config

config = load_config()

client = openai.OpenAI(api_key=config["openai_api_key"])

def generate_script(topic, style="educational", length="long"):
    print(f"[Script Generator] Generating script for topic: {topic}")
    prompt = (
        f"Write a {length}, {style} YouTube video script about '{topic}'. "
        f"Make it engaging, informative, and structured with an intro, main points, and conclusion."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional YouTube scriptwriter."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=2000
        )
        script = response.choices[0].message.content
        return script.strip()
    
    except Exception as e:
        print(f"[Script Generator] Error: {e}")
        return None
