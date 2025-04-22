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
# Replace with your own API key
RAPIDAPI_KEY = "782d6d8862msh8f2f93f8954c7bcp1d4295jsn49c7eca0cd55"
API_HOST = "youtube-info-download-api.p.rapidapi.com"

# Route to get download info (e.g., download URL)
@app.get("/download")
def get_download_link(video_url: str, format: str = "mp3", audio_quality: str = "128"):
    url = f"https://{API_HOST}/ajax/download.php"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": API_HOST
    }
    params = {
        "format": format,
        "add_info": "0",
        "url": video_url,
        "audio_quality": audio_quality
    }

    response = requests.get(url, headers=headers, params=params)
    
    # Log the response from RapidAPI for debugging
    print("API Response:", response.json())
    
    # Check if the download URL is in the response and return it
    if response.ok and 'download_url' in response.json():
        return response.json()
    else:
        return {"error": "Failed to retrieve download link"}


# Route to fetch video info
@app.get("/info")
def get_video_info(video_url: str):
    url = f"https://{API_HOST}/ajax/api.php"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": API_HOST
    }
    params = {
        "function": "i",
        "u": video_url
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()
