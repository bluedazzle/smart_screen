# coding: utf-8

from datetime import timedelta
from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'get-tank-value': {
        'task': 'drilling.tasks.get_tanks',
        'schedule': timedelta(seconds=10),
    },
    'get-inventory-record': {
        'task': 'drilling.tasks.get_inventory_record_task',
        'schedule': timedelta(seconds=60),
    },
}

CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_TIMEZONE = 'Asia/Shanghai'

CELERYD_CONCURRENCY = 4

CELERYD_MAX_TASKS_PER_CHILD = 300

CELERYD_FORCE_EXECV = True  # 非常重要,有些情况下可以防止死锁

CELERYD_PREFETCH_MULTIPLIER = 1
