#celery.py
import os
from celery import Celery
from celery.schedules import crontab

# Author: Dario Fervenza
# Copyright: Copyright (c) [2023], Dario Fervenza
# Version: 0.1
# Maintainer: Dario Fervenza
# Email: dario.fervenza.garcia@gmail.com
# Status: Development

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'interview.settings'
    )
app = Celery('interview')
app.config_from_object(
    'django.conf:settings',
    namespace='CELERY'
    )
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'run-periodic-task-every-15-minutes': {
        'task': 'my_app.tasks.guardar_temperaturas',
        'schedule': crontab(minute='*/35'),
    },
}

app.conf.update(
    CELERY_ENABLE_UTC=True,
    CELERY_TIMEZONE='UTC'
    )
@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
