# coding: utf-8
from __future__ import unicode_literals
from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView

from api.models import Site
from core.Mixin.CheckMixin import CheckSiteMixin
from core.Mixin.StatusWrapMixin import StatusWrapMixin, ERROR_DATA
from core.cache import client_redis_zhz
from core.dss.Mixin import JsonResponseMixin, MultipleJsonResponseMixin
from drilling.tasks import init_task, init_test
from super_admin.models import Task


class SiteListView(TemplateView):
    template_name = 'super_admin/site.html'


class TaskListView(TemplateView):
    template_name = 'super_admin/task.html'
