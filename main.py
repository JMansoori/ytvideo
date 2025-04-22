from flask import Flask, request, jsonify
from flask_cors import CORS
import http.client
import json
import urllib.parse
import re
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

RAPIDAPI_KEY = "782d6d8862msh8f2f93f8954c7bcp1d4295jsn49c7eca0cd55"
RAPIDAPI_HOST = "youtube-info-download-api.p.rapidapi.com"

def get_progress_link(video_url, format, audio_quality):
    conn = http.client.HTTPSConnection(RAPIDAPI_HOST)
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': RAPIDAPI_HOST
    }
    encoded_url = urllib.parse.quote(video_url, safe='')
    endpoint = f"/ajax/download.php?format={format}&add_info=0&url={encoded_url}&audio_quality={audio_quality}"
    
    conn.request("GET", endpoint, headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    
    try:
        json_data = json.loads(data)
        return json_data.get("progress_url")
    except:
        return None

def get_download_link(progress_url):
    try:
        # Extract path from the full progress URL
        parsed_url = urllib.parse.urlparse(progress_url)
        conn = http.client.HTTPSConnection(parsed_url.netloc)
        conn.request("GET", parsed_url.path)
        res = conn.getresponse()
        html = res.read().decode("utf-8")

        # Find the download_url="..." pattern
        match = re.search(r'download_url="([^"]+)"', html)
        if match:
            download_url = match.group(1).replace("\\/", "/")
            return download_url
        else:
            return None
    except:
        return None

@app.route("/download", methods=["GET"])
def download():
    video_url = request.args.get("video_url")
    format = request.args.get("format", "mp4")
    audio_quality = request.args.get("audio_quality", "128")

    if not video_url:
        return jsonify({"error": "Missing video_url"}), 400

    progress_url = get_progress_link(video_url, format, audio_quality)
    if not progress_url:
        return jsonify({"error": "Failed to get progress URL"}), 500

    time.sleep(2)  # Wait before progress_url responds with the link
    download_url = get_download_link(progress_url)

    if not download_url:
        return jsonify({"error": "Failed to retrieve download link"}), 500

    return jsonify({"download_url": download_url})

if __name__ == "__main__":
    app.run(debug=True)
