import os
import random
from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

CAT_API_URL = os.getenv("CAT_API_URL", "https://api.thecatapi.com/v1/images/search")
CAT_API_KEY = os.getenv("CAT_API_KEY")  # optional, improves rate limits

# Fallback URLs in case external API is unreachable (keep a few cute cats handy)
FALLBACK_CATS = [
    "https://placekitten.com/640/360",
    "https://placekitten.com/600/400",
    "https://placekitten.com/500/500",
    "https://placekitten.com/720/480",
    "https://placekitten.com/800/533",
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/cat")
def api_cat():
    headers = {}
    if CAT_API_KEY:
        headers["x-api-key"] = CAT_API_KEY

    try:
        r = requests.get(
            CAT_API_URL,
            params={"limit": 1, "mime_types": "jpg,png"},
            headers=headers,
            timeout=5,
        )
        r.raise_for_status()
        data = r.json()
        if isinstance(data, list) and data:
            return jsonify({"url": data[0].get("url")})
    except Exception:
        pass  # fall through to local fallback

    return jsonify({"url": random.choice(FALLBACK_CATS)})

@app.route("/healthz")
def healthz():
    return "ok", 200

if __name__ == "__main__":
    # Dev server (use gunicorn in container/production)
    app.run(host="0.0.0.0", port=5000)
