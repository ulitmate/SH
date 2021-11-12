from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab
from store.models import Schedule
import os, datetime

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storevictor.settings')

app = Celery('storevictor')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


#Schedule.objects.filter(sending_datetime__gte=datetime.datetime.now()).order_by('sending_datetime').last()

# app.conf.beat_schedule = {
#     # Executes every 30 minutes.
#     'every-30-minutes': {
#         'task': 'tasks.send_notification_email_task',
#         'schedule': crontab(minute='*/30'),
#         'args': (subject, body, discount_code, client_name, operator_first_name, dest_email)
#     },
# }