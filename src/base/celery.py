import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.dev')

app = Celery('base')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'Europe/Kiev'
app.autodiscover_tasks()
