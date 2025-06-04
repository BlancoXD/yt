import json
from pathlib import Path

MEMORY_PATH = Path("core/outputs/topic_memory.json")
MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)

def save_topic(topic):
    memory = load_memory()
    if topic not in memory:
        memory.append(topic)
        with open(MEMORY_PATH, "w") as f:
            json.dump(memory, f, indent=2)

def load_memory():
    if MEMORY_PATH.exists():
        with open(MEMORY_PATH, "r") as f:
            return json.load(f)
    return []

def clear_memory():
    if MEMORY_PATH.exists():
        MEMORY_PATH.unlink()
