import shutil
from pathlib import Path

EXPORTS = {
    "tiktok": "exports/tiktok",
    "instagram": "exports/instagram",
    "facebook": "exports/facebook"
}

def export_video(video_path, platform):
    target_dir = Path(EXPORTS.get(platform, "exports/other"))
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / Path(video_path).name
    shutil.copy(video_path, target_path)
    return str(target_path)
