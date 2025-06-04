import json
from core.script_generator import generate_script
from core.voiceover import synthesize_voice
from core.video_creator import create_video_from_script
from core.uploader import upload_video
from core.series_builder import build_series_title
from core.comments import auto_engage_comments
from core.topic_memory import remember_topic
from core.export import export_to_platforms
from core.a_b_tester import run_ab_test
from utils.helpers import slugify

with open("config.json", "r") as f:
    config = json.load(f)

def main():
    print("📽️  [YT Automation] Starting pipeline...")

    topic = input("🎯 Enter video topic: ").strip()
    script = generate_script(topic)
    title = build_series_title(topic)
    voice_path = synthesize_voice(script)
    video_path = create_video_from_script(script, voice_path)

    upload_result = upload_video(video_path, title, script)

    remember_topic(topic)
    auto_engage_comments(upload_result["video_id"])
    export_to_platforms(video_path)
    run_ab_test(video_path, title)

    print("✅ [YT Automation] Pipeline complete.")

if __name__ == "__main__":
    main()
