from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_with_django.settings')

app = Celery('celery_with_django')
app.conf.update(timezone = 'Asia/Kolkata')
app.config_from_object(settings, namespace='CELERY')

# CELERY BEAT SETTINGS
app.conf.beat_schedule = {     #cron

}

app.autodiscover_tasks()

@app.task(bind =True)
def debug_task(self):
    print(f'Request: {self.request!r}')