import os
from googleapiclient.discovery import build
import re

# Surakshit tareeke se API Key ko environment variable se lena
API_KEY = os.environ.get('YOUTUBE_API_KEY')
if not API_KEY:
    print("FATAL ERROR: YOUTUBE_API_KEY environment variable is not set.")
    # Agar key nahi hai to ek dummy key use karein, taki app crash na ho
    API_KEY = "dummy_key_so_app_does_not_crash"

# Build the service object only if the API key is not a dummy
youtube = None
if API_KEY != "dummy_key_so_app_does_not_crash":
    try:
        youtube = build('youtube', 'v3', developerKey=API_KEY)
    except Exception as e:
        print(f"Could not build YouTube service: {e}")


def get_channel_id_from_url(url):
    """Channel URL se Channel ID nikalta hai."""
    if not youtube:
        return None

    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/channel\/([a-zA-Z0-9_-]{24})',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/c\/([a-zA-Z0-9_-]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/@([a-zA-Z0-9_-]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/user\/([a-zA-Z0-9_-]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            # Agar @handle ya /c/ wala URL hai to ID search karni padegi
            if 'channel' not in pattern:
                search_term = match.group(1)
                try:
                    search_request = youtube.search().list(
                        part='snippet',
                        q=search_term,
                        type='channel',
                        maxResults=1
                    )
                    search_response = search_request.execute()
                    if search_response.get('items'):
                        return search_response['items'][0]['snippet']['channelId']
                except Exception as e:
                    print(f"Error searching for channel by handle/name: {e}")
                    return None
            else: # Agar seedha channel ID wala URL hai
                return match.group(1)
    return None

def get_channel_details(channel_id):
    """Channel ID se uski poori details nikalta hai."""
    if not youtube:
        return {'error': 'YouTube API service is not available.'}

    try:
        request = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        )
        response = request.execute()

        if not response.get('items'):
            return {'error': 'Channel not found.'}

        channel = response['items'][0]
        snippet = channel['snippet']
        statistics = channel['statistics']

        # Date ko format karna
        from datetime import datetime
        published_date = datetime.strptime(snippet['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
        
        return {
            'channelName': snippet['title'],
            'channelHandle': snippet.get('customUrl', 'N/A'),
            'subscribers': int(statistics.get('subscriberCount', 0)),
            'totalViews': int(statistics.get('viewCount', 0)),
            'totalVideos': int(statistics.get('videoCount', 0)),
            'thumbnail': snippet['thumbnails']['high']['url'],
            'publishedAt': published_date.strftime('%b %d, %Y'),
            'description': snippet['description']
        }
    except Exception as e:
        # Error ko handle karna
        print(f"An error occurred: {e}")
        return {'error': 'An error occurred while fetching channel data. The API key might be invalid or quota exceeded.'}
