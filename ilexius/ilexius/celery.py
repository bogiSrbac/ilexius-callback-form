import os
from celery import Celery
from django.conf import settings
from requests import Request, Session
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ilexius.settings')

app = Celery('ilexius')
app.conf.enable_utc = False
app.conf.update(timezone='Europe/Belgrade')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'archive-callbacks':{
        'task': 'customerServiceSupport.tasks.makeCallbacksRealizedCelery',
        'schedule': crontab(hour=20, day_of_week='mon-fri')
    },
    'archive-callbacks-saturday':{
        'task': 'customerServiceSupport.tasks.makeCallbacksRealizedCelery',
        'schedule': crontab(hour=13, day_of_week='sun')
    }
}