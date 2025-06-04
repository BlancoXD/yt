from core.topic_memory import load_memory

def build_series():
    memory = load_memory()
    if not memory:
        return []

    series = []
    for topic in memory:
        for i in range(1, 4):
            series.append(f"{topic} - Episode {i}")
    return series
