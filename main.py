from flask import Flask, request, jsonify
from flask_cors import CORS
import http.client
import json
import urllib.parse

# Load API credentials
with open("config.json") as config_file:
    config = json.load(config_file)

API_KEY = config["RAPIDAPI_KEY"]
API_HOST = "youtube-info-download-api.p.rapidapi.com"

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['GET'])
def download_video():
    video_url = request.args.get('video_url')
    format_ = request.args.get('format', 'mp3')
    audio_quality = request.args.get('audio_quality', '128')

    if not video_url:
        return jsonify({'error': 'Missing video_url'}), 400

    encoded_url = urllib.parse.quote(video_url, safe='')

    # Step 1: Request the download info
    conn = http.client.HTTPSConnection(API_HOST)
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': API_HOST
    }

    path = f"/ajax/download.php?format={format_}&add_info=0&url={encoded_url}&audio_quality={audio_quality}"
    conn.request("GET", path, headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")

    try:
        download_info = json.loads(data)
        progress_url = download_info.get("progress_url")

        if not progress_url:
            return jsonify({'error': 'Progress URL not found'}), 500

        # Step 2: Get the actual download URL
        parsed = urllib.parse.urlparse(progress_url)
        conn2 = http.client.HTTPSConnection(parsed.netloc)
        conn2.request("GET", parsed.path)
        res2 = conn2.getresponse()
        progress_data = res2.read().decode("utf-8")
        progress_info = json.loads(progress_data)

        raw_url = progress_info.get("download_url", "")
        download_url = raw_url.replace("\\/", "/") if raw_url else None

        if download_url:
            return jsonify({'download_url': download_url})
        else:
            return jsonify({'error': 'Download URL not found'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
