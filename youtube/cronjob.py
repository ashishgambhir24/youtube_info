from datetime import datetime
import logging
from video.youtube_apis import get_videos
from video.models import Thumbnail, Video
from youtube.settings import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def fetch_videos(published_after, topic):
    APIKEY = 'AIzaSyB4bxiE-XVs377A1C-YPL90xxOVaOP1_fk'
    next_page_token = None
    while True:
        api_resp = get_videos(published_after, topic, APIKEY, next_page_token)
        api_data = api_resp.json()
        videos_data = api_data['items']
        for video_data in videos_data:
            try:
                video = Video.objects.get(video_id=video_data['id']['videoId'])
                continue
            except Video.DoesNotExist:
                pass

            snippet = video_data['snippet']
            video = Video(
                video_id=video_data['id']['videoId'],
                etag=video_data['etag'],
                title=snippet['title'],
                description=snippet['description'],
                channel_id=snippet['channelId'],
                channel_title=snippet['channelTitle'],
                live_brodcast_content=snippet['liveBroadcastContent'],
                published_at=datetime.strptime(snippet['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
            )
            video.full_clean()
            video.save()

            thumbnails_data = snippet['thumbnails']
            for k,v in thumbnails_data.items():
                thumbnail = Thumbnail(
                    video=video,
                    type=k,
                    url=v['url'],
                    width=v['width'],
                    height=v['height']
                )
                thumbnail.full_clean()
                thumbnail.save()

            logger.info(f"video with etag {video_data['etag']} added 🔥🔥🔥🔥🔥🔥🔥")

        if api_data.get('nextPageToken', None):
            next_page_token = api_data['nextPageToken']
        else:
            break
