from flask import Flask, request, jsonify
import http.client
import time

app = Flask(__name__)

# Function to get progress URL
def get_progress_url(video_url, format="mp3", audio_quality="128"):
    conn = http.client.HTTPSConnection("youtube-info-download-api.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "782d6d8862msh8f2f93f8954c7bcp1d4295jsn49c7eca0cd55",
        'x-rapidapi-host': "youtube-info-download-api.p.rapidapi.com"
    }

    # Request to get the progress URL
    conn.request("GET", f"/ajax/download.php?format={format}&add_info=0&url={video_url}&audio_quality={audio_quality}", headers=headers)
    res = conn.getresponse()
    data = res.read()

    # Decode the response
    decoded_data = data.decode("utf-8")
    print("Progress URL Response:", decoded_data)

    # Extract the progress URL from the response (parse the decoded_data here)
    # You will need to adjust based on actual response format
    progress_url = decoded_data  # Replace with actual progress URL extraction logic

    return progress_url


# Function to get the final download URL from progress URL
def get_download_url(progress_url):
    conn = http.client.HTTPSConnection("pamela88.oceansaver.in")

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    conn.request("GET", progress_url, headers=headers)
    res = conn.getresponse()
    data = res.read()

    # Decode the data
    decoded_data = data.decode("utf-8")
    print("Download URL Response:", decoded_data)

    # Extract the download URL (parse the decoded_data here)
    download_url = decoded_data  # Replace with the actual logic to extract download_url

    # Fix the escaped '/' in download_url
    corrected_download_url = download_url.replace("\\/", "/")

    return corrected_download_url


@app.route('/download', methods=['GET'])
def download_video():
    video_url = request.args.get('video_url')
    format = request.args.get('format', 'mp3')
    audio_quality = request.args.get('audio_quality', '128')

    # Step 1: Get the progress URL
    progress_url = get_progress_url(video_url, format, audio_quality)

    # Step 2: Get the download URL from the progress URL
    download_url = get_download_url(progress_url)

    return jsonify({"download_url": download_url})


if __name__ == "__main__":
    app.run(debug=True)
