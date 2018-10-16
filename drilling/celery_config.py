# coding: utf-8

from drilling.db.session import config_oil_session
from core.util import conf

from datetime import timedelta
from celery.schedules import crontab

# CELERYBEAT_SCHEDULE = {
#     'get-tank-value': {
#         'task': 'drilling.tasks.get_tanks',
#         'schedule': timedelta(seconds=10),
#     },
#     'get-inventory-record': {
#         'task': 'drilling.tasks.get_inventory_record_task',
#         'schedule': timedelta(seconds=60),
#     },
# }

CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_TIMEZONE = 'Asia/Shanghai'

CELERYD_CONCURRENCY = 300

CELERYD_MAX_TASKS_PER_CHILD = 1000

CELERYD_FORCE_EXECV = True  # 非常重要,有些情况下可以防止死锁

CELERYD_PREFETCH_MULTIPLIER = 30

CELERY_TASK_RESULT_EXPIRES = 60 * 60  # 1 hour

CELERYD_LOG_LEVEL = "INFO"

config_oil_session(conf)
