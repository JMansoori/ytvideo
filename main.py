from flask import Flask, request, jsonify
import http.client
import json
import urllib.parse
import re

app = Flask(__name__)

# Load API key from config.json
with open("config.json") as f:
    config = json.load(f)
API_KEY = config["RAPIDAPI_KEY"]
API_HOST = config["RAPIDAPI_HOST"]

def get_progress_url(video_url, format, audio_quality):
    encoded_url = urllib.parse.quote(video_url, safe='')
    conn = http.client.HTTPSConnection(API_HOST)
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': API_HOST
    }

    path = f"/ajax/download.php?format={format}&add_info=0&url={encoded_url}&audio_quality={audio_quality}"
    conn.request("GET", path, headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")

    match = re.search(r'"progress_url"\s*:\s*"([^"]+)"', data)
    return match.group(1) if match else None

def get_download_url(progress_url):
    clean_url = progress_url.replace("\\/", "/")
    conn = http.client.HTTPSConnection("pamela88.oceansaver.in")  # Will be replaced dynamically
    path = clean_url.replace("https://pamela88.oceansaver.in", "")
    conn.request("GET", path)
    res = conn.getresponse()
    data = res.read().decode("utf-8")

    match = re.search(r'"download_url"\s*:\s*"([^"]+)"', data)
    return match.group(1).replace("\\/", "/") if match else None

@app.route("/download", methods=["GET"])
def download():
    video_url = request.args.get("video_url")
    format = request.args.get("format", "mp4")
    audio_quality = request.args.get("audio_quality", "128")

    progress_url = get_progress_url(video_url, format, audio_quality)
    if not progress_url:
        return jsonify({"error": "Failed to get progress URL"}), 500

    download_url = get_download_url(progress_url)
    if not download_url:
        return jsonify({"error": "Failed to get download URL"}), 500

    return jsonify({"download_url": download_url})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
