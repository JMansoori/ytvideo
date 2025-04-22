from flask import Flask, request, jsonify
from flask_cors import CORS
import http.client
import json

app = Flask(__name__)
CORS(app)  # This enables CORS for all domains by default

@app.route('/download', methods=['GET'])
def download():
    video_url = request.args.get('video_url')
    format = request.args.get('format', 'mp3')

    # Step 1: Encode the URL
    encoded_url = video_url.replace(":", "%3A").replace("/", "%2F").replace("?", "%3F").replace("=", "%3D").replace("&", "%26")

    conn = http.client.HTTPSConnection("youtube-info-download-api.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "782d6d8862msh8f2f93f8954c7bcp1d4295jsn49c7eca0cd55",
        'x-rapidapi-host': "youtube-info-download-api.p.rapidapi.com"
    }

    # Step 2: Get the progress URL
    progress_path = f"/ajax/download.php?format={format}&add_info=0&url={encoded_url}&audio_quality=128"
    conn.request("GET", progress_path, headers=headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))

    # Step 3: Extract progress API URL
    if 'progress_url' not in data:
        return jsonify({"error": "Progress URL not found"}), 500

    progress_url = data['progress_url'].replace("https://", "")
    conn = http.client.HTTPSConnection(progress_url.split("/")[0])
    conn.request("GET", "/" + "/".join(progress_url.split("/")[1:]))
    res = conn.getresponse()
    progress_data = json.loads(res.read().decode("utf-8"))

    # Step 4: Extract final download URL
    download_url = progress_data.get("download_url", "").replace("\\/", "/")
    if not download_url:
        return jsonify({"error": "Failed to retrieve download link"}), 500

    return jsonify({"download_url": download_url})

if __name__ == "__main__":
    app.run(debug=True)
