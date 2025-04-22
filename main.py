from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()
# Root route
@app.get("/")
def read_root():
    return {"message": "API is working"}

# CORS setup for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.zooobify.in"],  # Allow only this domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Route for handling the download request
@app.get("/download")
def get_download_link(video_url: str, format: str = "mp3", audio_quality: str = "128"):
    # YouTube Info Download API URL
    url = "https://youtube-info-download-api.p.rapidapi.com/ajax/download.php"
    
    headers = {
        "x-rapidapi-key": "your-rapidapi-key",  # Replace with your RapidAPI key
        "x-rapidapi-host": "youtube-info-download-api.p.rapidapi.com"
    }
    
    params = {
        "format": format,  # Audio/Video format (mp3, mp4, etc.)
        "add_info": "0",   # Don't add extra info
        "url": video_url,  # YouTube video URL
        "audio_quality": audio_quality  # Audio quality for mp3 (e.g., 128)
    }

    # Send request to RapidAPI
    response = requests.get(url, headers=headers, params=params)

    # Log the response to see what's being returned (For debugging)
    print("Response from RapidAPI:", response.json())

    response_data = response.json()

    # Check if download_url exists in the response
    if 'download_url' in response_data:
        return {"download_url": response_data['download_url']}
    else:
        return {"error": "Failed to retrieve download link"}
