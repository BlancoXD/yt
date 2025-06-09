from utils.config import load_config
from core.script_generator import generate_script
from core.voiceover import synthesize_voice
from core.video_creator import create_video
from core.uploader import upload_to_youtube
from core.comments import auto_engage_comments
from core.topic_memory import save_topic
from core.export import export_video
from core.a_b_tester import create_multiple_variants

config = load_config()

def main():
    print("📽️  [YT Automation] Starting pipeline...")

    topic = input("🎯 Enter video topic: ").strip()
    script = generate_script(topic)
    if not script:
        print("❌ [YT Automation] Failed to generate script. Exiting.")
        return

    title = topic
    voice_path = synthesize_voice(script)
    video_path = create_video(script, voice_path)

    video_id = upload_to_youtube(video_path, None, config)

    save_topic(topic)
    auto_engage_comments(video_id)
    export_video(video_path, "tiktok")
    create_multiple_variants(title)

    print("✅ [YT Automation] Pipeline complete.")

if __name__ == "__main__":
    main()
