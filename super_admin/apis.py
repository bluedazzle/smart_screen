# coding: utf-8
from __future__ import unicode_literals
from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView
from django.views.generic import ListView

from api.models import Site
from core.Mixin.CheckMixin import CheckSiteMixin
from core.Mixin.StatusWrapMixin import StatusWrapMixin, ERROR_DATA, ERROR_UNKNOWN
from core.cache import client_redis_zhz
from core.dss.Mixin import JsonResponseMixin, MultipleJsonResponseMixin
from drilling.const import TaskStatus
from drilling.init import update_init_progress
from drilling.tasks import init_task, init_test
from super_admin.models import Task


class SiteListView(StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = Site
    paginate_by = 20
    include_attr = ['name', 'slug', 'create_time', 'check', 'id']
    ordering = ('-create_time', 'check')


class SiteOverviewView(StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = Site
    paginate_by = 20
    include_attr = ['name', 'slug', 'msg', 'update_time', 'id', 'check']

    def get_queryset(self):
        queryset = super(SiteOverviewView, self).get_queryset().order_by('-create_time')
        map(self.get_site_status, queryset)
        return queryset

    @staticmethod
    def get_site_status(obj):
        data = client_redis_zhz.get('site_{0}'.format(obj.slug))
        if data:
            value_list = data.decode('utf-8').split('|$|')
            if len(value_list) >=2:
                msg, time = value_list[0], value_list[1]
            else:
                msg = time = ''
            setattr(obj, 'msg', msg)
            setattr(obj, 'update_time', time)


class TaskView(StatusWrapMixin, JsonResponseMixin, DetailView):
    model = Site

    def get(self, request, *args, **kwargs):
        slug = request.GET.get('slug', None)
        if slug:
            init_task.delay(slug)
            # init_test.delay(slug)
            return self.render_to_response({})
        self.message = '参数缺失'
        self.status_code = ERROR_DATA
        return self.render_to_response({})


class TaskListView(StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = Task
    paginate_by = 500

    def get_queryset(self):
        queryset = super(TaskListView, self).get_queryset().order_by('-create_time')
        map(self.get_task_detail, queryset)
        return queryset

    @staticmethod
    def get_task_detail(obj):
        data = client_redis_zhz.get(obj.task_id)
        if data:
            value_list = data.decode('utf-8').split('|$|')
            if len(value_list) >= 3:
                status, percent, msg = value_list[0], value_list[1], value_list[2]
            else:
                status = percent = msg = ''
            setattr(obj, 'status', int(status))
            setattr(obj, 'status_display', TaskStatus.get_display_name(int(status)))
            setattr(obj, 'percent', percent)
            setattr(obj, 'msg', msg)


class TaskCancelView(StatusWrapMixin, JsonResponseMixin, DetailView):
    model = Task

    def get(self, request, *args, **kwargs):
        from celery import current_app, app
        task_id = request.GET.get('id')
        if task_id:
            current_app.control.revoke(task_id, terminate=True)
            update_init_progress(task_id, 100, '任务被终止', TaskStatus.finish)
            return self.render_to_response({})
        self.message = '终止失败'
        self.status_code = ERROR_UNKNOWN
        return self.render_to_response({})
