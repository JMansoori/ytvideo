<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Downloader</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>
<body>
    <h1>YouTube Video Downloader</h1>
    <label for="video_url">Video URL: </label>
    <input type="text" id="video_url" placeholder="Enter YouTube Video URL">
    <label for="format">Format: </label>
    <select id="format">
        <option value="mp3">MP3</option>
        <option value="mp4">MP4</option>
    </select>
    <label for="audio_quality">Audio Quality: </label>
    <input type="text" id="audio_quality" placeholder="Audio Quality (e.g., 128)">
    <button onclick="downloadVideo()">Download</button>

    <p id="message"></p>

    <script>
        function downloadVideo() {
            var video_url = document.getElementById('video_url').value;
            var format = document.getElementById('format').value;
            var audio_quality = document.getElementById('audio_quality').value;

            if (!video_url) {
                document.getElementById('message').innerText = "Please enter a video URL.";
                return;
            }

            // Show message for progress
            document.getElementById('message').innerText = "Fetching download link...";

            // Make the AJAX request to the Flask backend
            $.ajax({
                url: 'https://your-render-app-url.onrender.com/download',  // Replace with your Render URL
                method: 'GET',
                data: {
                    video_url: video_url,
                    format: format,
                    audio_quality: audio_quality
                },
                success: function(response) {
                    var downloadUrl = response.download_url;

                    if (downloadUrl) {
                        document.getElementById('message').innerHTML = 'Download ready! <a href="' + downloadUrl + '" target="_blank">Click here to download</a>';
                    } else {
                        document.getElementById('message').innerText = "Failed to retrieve download link. Please try again.";
                    }
                },
                error: function() {
                    document.getElementById('message').innerText = "Error occurred. Please try again.";
                }
            });
        }
    </script>
</body>
</html>
