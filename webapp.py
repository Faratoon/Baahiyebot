"""
webapp.py  –  Flask server for the Mini Web App
Serves the Telegram WebApp (index.html) for testing
"""
import os
from flask import Flask, send_from_directory

app = Flask(__name__)

WEBAPP_DIR = os.path.join(os.path.dirname(__file__), "telebot1", "webapp")


@app.route("/")
def index():
    return send_from_directory(WEBAPP_DIR, "index.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(WEBAPP_DIR, path)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print(f"🌐 WebApp running at http://localhost:{port}")
    app.run(host="0.0.0.0", port=port)
