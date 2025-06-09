from pathlib import Path
import json

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.json"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)
