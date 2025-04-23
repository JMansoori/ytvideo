# app.py

from flask import Flask, request, jsonify
import http.client
from flask_cors import CORS
import json
import urllib.parse
from config import RAPIDAPI_KEY, RAPIDAPI_HOST

app = Flask(__name__)
CORS(app, origins=["https://youtube-downloader-api-i44x.onrender.com"])

def make_rapidapi_request(endpoint):
    conn = http.client.HTTPSConnection(RAPIDAPI_HOST)
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': RAPIDAPI_HOST
    }
    conn.request("GET", endpoint, headers=headers)
    res = conn.getresponse()
    return res.read()

@app.route('/api/info', methods=['GET'])
def get_info():
    video_url = request.args.get('url')
    encoded_url = urllib.parse.quote(video_url)
    endpoint = f"/ajax/api.php?function=i&u={encoded_url}"
    data = make_rapidapi_request(endpoint)
    return jsonify(json.loads(data.decode('utf-8')))

@app.route('/api/download', methods=['GET'])
def get_download():
    video_url = request.args.get('url')
    format_ = request.args.get('format', '720')
    encoded_url = urllib.parse.quote(video_url)

    download_endpoint = f"/ajax/download.php?format={format_}&add_info=0&url={encoded_url}&audio_quality=128"
    initial_response = json.loads(make_rapidapi_request(download_endpoint).decode('utf-8'))

    progress_url = initial_response.get('progress_url')
    if not progress_url:
        return jsonify({"error": "Progress URL not found."}), 400

    parsed_progress_url = urllib.parse.urlparse(progress_url)
    progress_conn = http.client.HTTPSConnection(parsed_progress_url.netloc)
    progress_conn.request("GET", parsed_progress_url.path + "?" + parsed_progress_url.query, headers={
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': RAPIDAPI_HOST
    })

    progress_data = json.loads(progress_conn.getresponse().read().decode("utf-8"))

    if progress_data.get("success") == 1 and progress_data.get("progress") == 1000:
        download_url = progress_data.get("download_url", "").replace("\\/", "/")
        return jsonify({"download_url": download_url})
    else:
        return jsonify({"error": "Download not ready or failed.", "details": progress_data}), 400

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
