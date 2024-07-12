import os
from celery import Celery
from celery.schedules import crontab
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'billboard.settings')
 
app = Celery('billboard')
app.config_from_object('django.conf:settings', namespace = 'CELERY')
app.autodiscover_tasks()



app.conf.beat_schedule = {
    'send_weekly_posts_friday_8am': {
        'task': 'tasks.weekly_posts_task',
        'schedule': crontab(hour=8, minute=0, day_of_week='friday'),
    },
}