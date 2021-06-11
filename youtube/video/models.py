from datetime import datetime
import pytz
from django.db import models
from django.forms.models import model_to_dict
from enum import Enum

class ThumbnailType(Enum):
    default = 'default'
    medium = 'medium'
    high = 'high'

class Video(models.Model):
    video_id = models.CharField(max_length=40, unique=True)
    etag = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    channel_id = models.CharField(max_length=50)
    channel_title = models.CharField(max_length=100)
    live_brodcast_content = models.CharField(max_length=50)
    published_at = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def jsonify(self):
        data = model_to_dict(self, exclude['video_id', 'etag', 'channel_id'])
        data['url'] = f'https://www.youtube.com/watch?v={self.video_id}'
        thumbnails_data = {}
        thumbnails = self.thumbnail_set.all()
        for thumbnail in thumbernails:
            thumbnails_data.update(thumbnail.jsonify())

        data['thumbnails'] = thumbnails_data
        # data['published_at'] = str(datetime.strptime(
        #     self.published_at, "%Y-%m-%dT%H:%M:%SZ"
        # ).replace(
        #     tzinfo=pytz.UTC
        # ).astimezone(
        #     pytz.timezone("Asia/Calcutta")
        # ))
        data['published_at'] = str(self.published_at)
        return data

class Thumbnail(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=20,
        choices=[(tag.name, tag.value) for tag in ThumbnailType]
    )
    url = models.URLField()
    width = models.IntegerField()
    height = models.IntegerField()

    def jsonify(self):
        data = model_to_dict(self, exclude=['video', 'type'])
        return {self.type: data}