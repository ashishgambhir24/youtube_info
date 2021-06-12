from datetime import datetime, timedelta
import logging
import time
import random
from video.youtube_apis import get_videos
from video.models import Thumbnail, Video
from youtube.celery import app
from youtube.constants import YOUTUBE_APIKEYS, CRONJOB_INTEVAL
from youtube.settings import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@app.task
def fetch_videos(published_after, topic):
    APIKEY = random.choice(YOUTUBE_APIKEYS)
    next_page_token = None
    while True:
        api_resp = get_videos(published_after, topic, APIKEY, next_page_token)
        if api_resp.status_code == 403:
            logger.info(api_resp.json(), f'APIKEY: {APIKEY}', '❌❌❌❌❌❌❌❌')
            APIKEY = random.choice(YOUTUBE_APIKEYS)
            continue

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

def datetime_to_str(dt):
    return datetime.strftime(dt, "%Y-%m-%dT%H:%M:%SZ")

@app.task
def start_cronjob():
    published_after = None
    keyword = 'sport' # Here we specify topic of video to be fetched
    while True:
        try:
            current_time = datetime.now()
            if not published_after:
                published_after = datetime_to_str(current_time - timedelta(seconds=CRONJOB_INTEVAL))

            fetch_videos.apply_async([published_after, keyword])
            published_after = datetime_to_str(current_time)
            time.sleep(CRONJOB_INTEVAL)
        except Exception as e:
            print(e)
            pass

if __name__ == "cronjob":
    start_cronjob.apply_async(countdown=30)
