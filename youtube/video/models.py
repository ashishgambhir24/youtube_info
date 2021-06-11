from datetime import datetime
import pytz
from django.db import models
from django.forms.models import model_to_dict
from enum import Enum

class ThumbernailType(Enum):
    default = 'default'
    medium = 'medium'
    high = 'high'

class Thumbernail(models.Model):
    type = models.CharField(
        max_length=20,
        choices=[(tag.name, tag.value) for tag in ThumbernailType]
    )
    url = models.URLField()
    width = models.IntegerField()
    height = models.IntegerField()

    def jsonify(self):
        data = model_to_dict(self, exclude=['type'])
        return {self.type: data}


class Video(models.Model):
    video_id = models.CharField(max_length=40, unique=True)
    etag = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    discription = models.TextField()
    thumbernails = models.ManyToManyField(Thumbernail)
    channel_id = models.CharField(max_length=50)
    channel_title = models.CharField(max_length=100)
    live_brodcast_content = models.CharField(max_length=50)
    published_at = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def jsonify(self):
        data = model_to_dict(self, exclude['video_id', 'etag', 'thumbernails', 'channel_id'])
        data['url'] = f'https://www.youtube.com/watch?v={self.video_id}'
        thumbernails_data = {}
        thumbernails = self.thumbernail_set.all()
        for thumbernail in thumbernails:
            thumbernails_data.update(thumbernail.jsonify())

        data['thumbernails'] = thumbernails_data
        data['published_at'] = str(datetime.strptime(
            self.published_at, "%Y-%m-%dT%H:%M:%SZ"
        ).replace(
            tzinfo=pytz.UTC
        ).astimezone(
            pytz.timezone("Asia/Calcutta")
        ))
        return data
