from googleapiclient.discovery import build
import re

def parse_channel_input(input_string):
    input_string = input_string.strip()
    if input_string.startswith('@'):
        return input_string[1:]
    
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/(?:channel\/|c\/|@|user\/)?([a-zA-Z0-9_.-]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, input_string)
        if match:
            return match.group(1)
            
    return input_string

def get_channel_details(api_key, channel_input):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        clean_input = parse_channel_input(channel_input)
        if not clean_input:
            return {'error': 'Invalid YouTube Channel URL or Handle.'}

        search_param = {}
        if clean_input.startswith('UC') and len(clean_input) == 24:
            search_param['id'] = clean_input
        else:
            request = youtube.search().list(
                part="snippet", q=clean_input, type="channel", maxResults=1
            )
            response = request.execute()
            if not response.get('items'):
                return {'error': f"Channel with handle '{clean_input}' not found."}
            search_param['id'] = response['items'][0]['id']['channelId']

        request = youtube.channels().list(
            part="snippet,statistics", **search_param
        )
        response = request.execute()

        if not response.get('items'):
            return {'error': 'Channel details not found. Please check the input.'}

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
        print(f"YouTube API Error: {e}")
        return {'error': 'An error occurred with the YouTube API. Key might be invalid or quota exceeded.'}