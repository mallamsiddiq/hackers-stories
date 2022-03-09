import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seedtest.settings')

app = Celery('seedtest')

app.config_from_object('django.conf:settings', namespace='CELERY')







app.conf.beat_schedule = {
    'add-every-continuesly-at-1min': {
        'task': 'blog.tasks.create_items_from_api_beat_latest',
<<<<<<< HEAD
        'schedule': 20.0
=======
        'schedule': 60*5
>>>>>>> f66bbbf (commit changes to doc)
        # 'schedule': crontab(hour=0, minute=46, day_of_month=19, month_of_year = 6),
        #'args': (2,)
    }
    
}

app.conf.timezone = 'UTC'






# Load task modules from all registered Django apps.







app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')