from flask import Flask, request, jsonify, render_template
import json
import os
import subprocess

app = Flask(__name__)

CONFIG_PATH = "config.json"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/load-config")
def load_config():
    if not os.path.exists(CONFIG_PATH):
        return jsonify({})
    with open(CONFIG_PATH, "r") as f:
        return jsonify(json.load(f))

@app.route("/save-config", methods=["POST"])
def save_config():
    data = request.json
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=2)
    return jsonify({"status": "success"})

@app.route("/run-module", methods=["POST"])
def run_module():
    data = request.json
    module_name = data.get("module")
    print(f"[Dashboard] Running module: {module_name}")

    try:
        if module_name == "run_all":
            result = subprocess.run(["python", "main.py"], capture_output=True, text=True)
        elif module_name == "dashboard":
            result = subprocess.run(["python", "dashboard/app.py"], capture_output=True, text=True)
        else:
            result = subprocess.run(["python", f"core/{module_name}.py"], capture_output=True, text=True)

        return jsonify({
            "status": "done",
            "output": result.stdout,
            "error": result.stderr
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/get-modules")
def get_modules():
    modules = [f.replace(".py", "") for f in os.listdir("core") if f.endswith(".py")]
    return jsonify(modules)

# ---------- Topic Memory ----------
@app.route("/topics")
def get_topics():
    from core.topic_memory import load_memory
    return jsonify(load_memory())

@app.route("/add-topic", methods=["POST"])
def add_topic():
    from core.topic_memory import save_topic
    data = request.json
    save_topic(data.get("topic"))
    return jsonify({"status": "saved"})

@app.route("/clear-topics", methods=["POST"])
def clear_topics():
    from core.topic_memory import clear_memory
    clear_memory()
    return jsonify({"status": "cleared"})

# ---------- Video Series ----------
@app.route("/build-series")
def build_series():
    from core.series_builder import build_series
    return jsonify(build_series())

# ---------- Export ----------
@app.route("/export", methods=["POST"])
def export_video_route():
    from core.export import export_video
    data = request.json
    path = export_video(data.get("video_path"), data.get("platform"))
    return jsonify({"status": "exported", "path": path})

# ---------- Niche Discovery ----------
@app.route("/discover-niche")
def discover_niche():
    from core.discover import fetch_google_trends
    return jsonify({"trends": fetch_google_trends()})

@app.route("/autocomplete")
def autocomplete():
    from core.discover import youtube_autocomplete
    q = request.args.get("q", "")
    return jsonify({"suggestions": youtube_autocomplete(q)})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
