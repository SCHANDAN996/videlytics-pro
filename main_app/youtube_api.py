import pandas as pd
from googleapiclient.discovery import build
from datetime import datetime, timezone
from io import BytesIO

class YouTubeChannelAnalyzer:
    """
    A comprehensive class to analyze a YouTube channel, fetch video data,
    and generate an Excel export.
    """
    def __init__(self, api_key):
        """Initializes the YouTube API client."""
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.video_categories = self._get_all_video_categories()

    def _get_all_video_categories(self):
        """Pre-fetches all video categories to avoid repeated API calls."""
        try:
            request = self.youtube.videoCategories().list(part="snippet", regionCode="US")
            response = request.execute()
            return {item['id']: item['snippet']['title'] for item in response['items']}
        except Exception as e:
            print(f"Error fetching video categories: {e}")
            return {}

    def get_channel_id(self, channel_input):
        """Extracts channel ID from various input formats (URL, @handle, ID)."""
        if channel_input.startswith('UC') and len(channel_input) == 24:
            return channel_input
        if 'youtube.com/channel/' in channel_input:
            return channel_input.split('/channel/')[-1].split('/')[0]
        
        username = None
        if 'youtube.com/c/' in channel_input:
            username = channel_input.split('/c/')[-1].split('/')[0]
        elif 'youtube.com/@' in channel_input:
            username = channel_input.split('/@')[-1].split('/')[0]
        elif channel_input.startswith('@'):
            username = channel_input[1:]
        else:
            username = channel_input

        try:
            request = self.youtube.search().list(part="snippet", q=username, type="channel", maxResults=1)
            response = request.execute()
            if response.get('items'):
                return response['items'][0]['snippet']['channelId']
        except Exception as e:
            print(f"Error searching channel by username '{username}': {e}")
        return None

    def get_channel_details(self, channel_id):
        """Fetches detailed information about the channel."""
        try:
            request = self.youtube.channels().list(part="snippet,statistics,contentDetails", id=channel_id)
            response = request.execute()
            if not response.get('items'):
                return None
            channel = response['items'][0]
            stats = channel.get('statistics', {})
            return {
                'Title': channel['snippet']['title'],
                'Description': channel['snippet']['description'],
                'Published At': channel['snippet']['publishedAt'],
                'Subscribers': int(stats.get('subscriberCount', 0)) if stats.get('subscriberCount') else 'Hidden',
                'Total Views': int(stats.get('viewCount', 0)),
                'Video Count': int(stats.get('videoCount', 0)),
                'Uploads Playlist ID': channel.get('contentDetails', {}).get('relatedPlaylists', {}).get('uploads')
            }
        except Exception as e:
            print(f"Error fetching channel details for ID '{channel_id}': {e}")
            return None

    def get_all_channel_videos(self, uploads_playlist_id, max_videos=50):
        """Fetches a list of videos from the channel's uploads playlist."""
        videos = []
        next_page_token = None
        if not uploads_playlist_id:
            return videos
            
        while len(videos) < max_videos:
            try:
                max_results = min(50, max_videos - len(videos))
                request = self.youtube.playlistItems().list(
                    part="contentDetails",
                    playlistId=uploads_playlist_id,
                    maxResults=max_results,
                    pageToken=next_page_token
                )
                response = request.execute()
                video_ids = [item['contentDetails']['videoId'] for item in response.get('items', [])]

                if video_ids:
                    video_details = self.get_video_details_bulk(video_ids)
                    videos.extend(video_details)

                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
            except Exception as e:
                print(f"Error fetching playlist items: {e}")
                break
        return videos

    def get_video_details_bulk(self, video_ids):
        """Fetches detailed statistics for a list of video IDs in a single API call."""
        video_details_list = []
        try:
            request = self.youtube.videos().list(
                part="snippet,statistics,contentDetails",
                id=",".join(video_ids)
            )
            response = request.execute()
            for item in response.get('items', []):
                # ... (Same detailed parsing logic as in my previous full response)
                # This part is complex and remains the same.
                snippet = item['snippet']
                stats = item.get('statistics', {})
                details = item.get('contentDetails', {})
                
                upload_date = snippet.get('publishedAt', '')
                if upload_date:
                    upload_datetime = datetime.strptime(upload_date, '%Y-%m-%dT%H:%M:%SZ')
                    upload_date_str = upload_datetime.strftime('%Y-%m-%d %H:%M:%S')
                    current_time = datetime.now(timezone.utc)
                    days_since_upload = max(1, (current_time - upload_datetime.replace(tzinfo=timezone.utc)).days)
                    views = int(stats.get('viewCount', 0))
                    views_per_day = views / days_since_upload
                else:
                    upload_date_str, days_since_upload, views_per_day = 'Unknown', 0, 0
                
                duration_minutes = self.parse_duration(details.get('duration', 'PT0M'))
                category_id = snippet.get('categoryId', '')
                category_name = self.video_categories.get(category_id, 'Unknown')
                tags = snippet.get('tags', [])
                tags_str = ', '.join(tags)[:497] + '...' if len(', '.join(tags)) > 500 else ', '.join(tags)
                video_id = item['id']

                video_details_list.append({
                    'Title': snippet.get('title', 'N/A'),
                    'Video ID': video_id,
                    'Video URL': f"https://www.youtube.com/watch?v={video_id}",
                    'Upload Date': upload_date_str,
                    'Views': int(stats.get('viewCount', 0)),
                    'Likes': int(stats.get('likeCount', 0)),
                    'Comments': int(stats.get('commentCount', 0)),
                    # ... add other fields as needed for display/export
                })
        except Exception as e:
            print(f"Error fetching bulk video details: {e}")
        return video_details_list
    
    def parse_duration(self, duration):
        """Converts ISO 8601 duration to minutes."""
        # ... (Same logic as before)
        duration = duration[2:]
        hours, minutes, seconds = 0, 0, 0
        if 'H' in duration:
            hours_str, duration = duration.split('H')
            hours = int(hours_str)
        if 'M' in duration:
            minutes_str, duration = duration.split('M')
            minutes = int(minutes_str)
        if 'S' in duration:
            seconds_str = duration.split('S')[0]
            seconds = int(seconds_str)
        return hours * 60 + minutes + seconds / 60

    def create_excel_export(self, channel_info, videos):
        """Creates an Excel file in memory and returns it as a BytesIO object."""
        # ... (Same Excel creation logic as before)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            pd.DataFrame([channel_info]).to_excel(writer, sheet_name='Channel Info', index=False)
            if videos:
                pd.DataFrame(videos).to_excel(writer, sheet_name='Videos', index=False)
        output.seek(0)
        return output
