from googleapiclient.discovery import build
import re

def get_channel_id_from_url(url):
    """YouTube URL se Channel ID ya Custom Name nikalne ka function."""
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/channel\/([a-zA-Z0-9_-]{24})',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/c\/([a-zA-Z0-9_-]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/@([a-zA-Z0-9_-]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/user\/([a-zA-Z0-9_-]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_channel_details(api_key, channel_input):
    """Channel ki details nikalne ka function."""
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        channel_id_or_name = get_channel_id_from_url(channel_input)
        if not channel_id_or_name:
            return {'error': 'Invalid YouTube Channel URL format.'}

        search_param = {}
        # Agar yeh ek aam Channel ID hai
        if channel_id_or_name.startswith('UC') and len(channel_id_or_name) == 24:
            search_param['id'] = channel_id_or_name
        # Agar yeh ek custom URL (/c/ ya /@) hai
        else:
            # Custom URL se Channel ID dhoondhne ke liye search API ka istemal karein
            request = youtube.search().list(
                part="snippet",
                q=channel_id_or_name,
                type="channel",
                maxResults=1
            )
            response = request.execute()
            if not response.get('items'):
                return {'error': 'Channel not found with that custom URL.'}
            # Asli Channel ID mil gayi
            search_param['id'] = response['items'][0]['id']['channelId']


        # Ab asli Channel ID se channel ki details nikalein
        request = youtube.channels().list(
            part="snippet,statistics",
            **search_param
        )
        response = request.execute()

        if not response.get('items'):
            return {'error': 'Channel not found. Please check the URL.'}

        channel = response['items'][0]
        stats = channel.get('statistics', {})
        
        return {
            'title': channel['snippet']['title'],
            'thumbnail': channel['snippet']['thumbnails']['default']['url'],
            'subscribers': stats.get('subscriberCount', '0'),
            'views': stats.get('viewCount', '0'),
            'videos': stats.get('videoCount', '0'),
            'channelId': channel['id']
        }
    except Exception as e:
        # Asli error ko server par log karein (debugging ke liye)
        print(f"YouTube API Error: {e}")
        # User ko ek saral error message dein
        return {'error': 'An error occurred while fetching data from YouTube API. The API key might be invalid or quota exceeded.'}