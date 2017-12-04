# coding: utf-8

from datetime import timedelta
from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'get-tank-value': {
        'task': 'smart_screen.drilling.tasks.test_tank',
        'schedule': timedelta(seconds=10),
    },
}

CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_TIMEZONE = 'Asia/Shanghai'

CELERYD_CONCURRENCY = 24

CELERYD_MAX_TASKS_PER_CHILD = 300

CELERYD_FORCE_EXECV = True  # 非常重要,有些情况下可以防止死锁

CELERYD_PREFETCH_MULTIPLIER = 1
