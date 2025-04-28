import os
from googleapiclient.discovery import build
import requests

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# YouTube search
def search_youtube_tutorials(tool_name):
    api_key = os.getenv("YOUTUBE_API_KEY")
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.search().list(
        q=f"{tool_name} tutorial",
        part='snippet',
        maxResults=2,
        type='video'
    )
    response = request.execute()

    tutorials = []
    for item in response.get('items', []):
        video_id = item['id']['videoId']
        link = f"https://www.youtube.com/watch?v={video_id}"
        tutorials.append(link)

    return tutorials
