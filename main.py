from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import http.client
import json
import urllib.parse

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load API key and host from config
with open('config.json') as f:
    config = json.load(f)

API_KEY = config['RAPIDAPI_KEY']
API_HOST = config['RAPIDAPI_HOST']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['GET'])
def download():
    video_url = request.args.get('video_url')
    format = request.args.get('format')
    audio_quality = request.args.get('audio_quality')

    if not video_url or not format:
        return jsonify({"error": "Missing parameters"}), 400

    encoded_url = urllib.parse.quote(video_url, safe='')
    path = f"/ajax/download.php?format={format}&add_info=0&url={encoded_url}&audio_quality={audio_quality}"

    conn = http.client.HTTPSConnection(API_HOST)
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': API_HOST
    }
    conn.request("GET", path, headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")

    try:
        json_data = json.loads(data)
        progress_url = json_data.get('progress_url')
        if not progress_url:
            return jsonify({"error": "Progress URL not found"}), 500

        # Get final download_url
        final_host = progress_url.replace("https://", "").split("/")[0]
        final_path = "/" + "/".join(progress_url.split("/")[3:])

        conn2 = http.client.HTTPSConnection(final_host)
        conn2.request("GET", final_path)
        res2 = conn2.getresponse()
        final_data = res2.read().decode("utf-8")
        final_json = json.loads(final_data)
        download_url = final_json.get("download_url", "").replace("\\/", "/")

        if not download_url:
            return jsonify({"error": "Download URL not found"}), 500

        return jsonify({"download_url": download_url})

    except Exception as e:
        return jsonify({"error": "Failed to retrieve download link", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
