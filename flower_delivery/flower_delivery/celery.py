from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_delivery.settings')

app = Celery('flower_delivery')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'send-daily-sales-report': {
        'task': 'core.tasks.send_daily_sales_report',
        'schedule': crontab(hour=8, minute=0),  # Каждый день в 8 утра
    },
}

