# app.py
from flask import Flask, request, jsonify
import http.client
import json
from config import RAPIDAPI_KEY, RAPIDAPI_HOST

app = Flask(__name__)

def call_api(endpoint):
    conn = http.client.HTTPSConnection(RAPIDAPI_HOST)
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': RAPIDAPI_HOST
    }
    conn.request("GET", endpoint, headers=headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

@app.route('/get_info', methods=['GET'])
def get_info():
    video_url = request.args.get('url')
    endpoint = f"/ajax/api.php?function=i&u={video_url}"
    return jsonify(call_api(endpoint))

@app.route('/get_download', methods=['GET'])
def get_download():
    video_url = request.args.get('url')
    format_ = request.args.get('format', '720')
    endpoint = f"/ajax/download.php?format={format_}&add_info=0&url={video_url}&audio_quality=128"
    result = call_api(endpoint)

    # Extract progress URL
    progress_url = result.get("progress_url", "")
    if progress_url:
        conn = http.client.HTTPSConnection(RAPIDAPI_HOST)
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': RAPIDAPI_HOST
        }
        conn.request("GET", progress_url, headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        if data.get("success") == 1 and data.get("progress") == 1000:
            download_url = data.get("download_url", "").replace("\\/", "/")
            return jsonify({"download_url": download_url})
    return jsonify({"error": "Download not ready or failed."})

if __name__ == '__main__':
   
    port = int(os.environ.get("PORT", 10000))  # Fallback to 10000
    app.run(host="0.0.0.0", debug=True, port=port)
