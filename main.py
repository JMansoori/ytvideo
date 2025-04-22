from flask import Flask, request, jsonify
from flask_cors import CORS
import http.client
import json

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['GET'])
def download():
    video_url = request.args.get('video_url')
    format_ = request.args.get('format', 'mp4')
    audio_quality = request.args.get('audio_quality', '128')

    if not video_url:
        return jsonify({"error": "Missing video URL"}), 400

    try:
        conn = http.client.HTTPSConnection("youtube-info-download-api.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': '782d6d8862msh8f2f93f8954c7bcp1d4295jsn49c7eca0cd55',  # Replace with your actual key
            'x-rapidapi-host': 'youtube-info-download-api.p.rapidapi.com'
        }

        # Format the request path
        encoded_url = video_url.replace(':', '%3A').replace('/', '%2F').replace('?', '%3F').replace('=', '%3D').replace('&', '%26')
        path = f"/ajax/download.php?format={format_}&add_info=0&url={encoded_url}&audio_quality={audio_quality}"

        conn.request("GET", path, headers=headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")

        # Check if "download_url" exists in response
        try:
            download_data = json.loads(data)
            progress_url = download_data.get("progress_url")
        except Exception:
            return jsonify({"error": "Unexpected response format from RapidAPI"}), 500

        if not progress_url:
            return jsonify({"error": "No progress URL returned"}), 500

        # Fetch progress to get final download URL
        conn.request("GET", progress_url, headers=headers)
        res2 = conn.getresponse()
        progress_data = res2.read().decode("utf-8")

        try:
            progress_json = json.loads(progress_data)
            raw_url = progress_json.get("download_url", "")
            clean_url = raw_url.replace("\\/", "/")
        except Exception:
            return jsonify({"error": "Could not parse progress response"}), 500

        return jsonify({"download_url": clean_url})

    except Exception as e:
        print("Server Error:", str(e))
        return jsonify({"error": "Failed to retrieve download link"}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
