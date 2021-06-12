from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube.settings')
app = Celery('youtube', broker=settings.BROKER_URL)
app.conf["accept_content"]=['json']
app.conf["result_serializer"]='json'
app.conf["task_serializer"]='json'

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
