# coding: utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from api.models import BaseModel, Site


class CeleryLog(BaseModel):
    status_choices = [
        (0, '失败'),
        (1, '正常'),
    ]

    task_choices = [
        (0, '初始化任务'),
        (1, '定时任务'),
    ]

    task_id = models.CharField(max_length=64)
    status = models.IntegerField(default=1, choices=status_choices)
    task_type = models.IntegerField(default=1, choices=task_choices)
    err_info = models.TextField(null=True, blank=True)
    belong = models.ForeignKey(Site, related_name='site_celery_logs', null=True, blank=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return '{0}-{1}-{2}-{3}'.format(self.belong.name, self.status, self.task_type, self.create_time)


class Task(BaseModel):
    task_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=64)
    belong = models.ForeignKey(Site, related_name='site_celery_tasks', null=True, blank=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return '{0}-{1}-{2}'.format(self.belong.name, self.name, self.create_time)
