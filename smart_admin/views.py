# coding: utf-8
from __future__ import unicode_literals

# Create your views here.
import random
import string

import time

import logging

from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import View

from SmartScreen.settings import STATIC_ROOT
from drilling.utils import generate_hash
from smart_admin.models import Account
from api.models import GoodsInventory, Site
from core.Mixin.CheckMixin import CheckAdminPermissionMixin
from core.Mixin.StatusWrapMixin import StatusWrapMixin, INFO_NO_EXIST, ERROR_PASSWORD, ERROR_DATA, ERROR_UNKNOWN
from core.dss.Mixin import MultipleJsonResponseMixin, JsonResponseMixin


class AdminLoginView(StatusWrapMixin, JsonResponseMixin, DetailView):
    model = Account
    http_method_names = ['post']
    include_attr = ['name', 'token', 'belong', 'slug']
    foreign = True

    @staticmethod
    def create_token(count=32):
        return string.join(
            random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcba',
                          count)).replace(" ", "")

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        password = request.POST.get('password')
        if name and password:
            try:
                obj = self.model.objects.get(name=name)
                if obj.check_password(password):
                    obj.token = self.create_token()
                    obj.save()
                    return self.render_to_response({"account": obj})
                self.message = '密码错误'
                self.status_code = ERROR_PASSWORD
                return self.render_to_response()
            except Exception as e:
                self.message = '账号不存在'
                self.status_code = INFO_NO_EXIST
                return self.render_to_response()


class InventoryListView(CheckAdminPermissionMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = GoodsInventory
    paginate_by = 20

    def get_queryset(self):
        queryset = super(InventoryListView, self).get_queryset()
        queryset.filter(belong=self.site).order_by('-original_create_time')
        return queryset


class SiteInfoView(CheckAdminPermissionMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    model = Site
    http_method_names = ['get', 'post']
    include_attr = ['name', 'slug', 'info']

    def get(self, request, *args, **kwargs):
        return self.render_to_response({'site': self.site})

    def post(self, request, *args, **kwargs):
        content = request.POST.get('content')
        self.site.info = content
        self.site.save()
        return self.render_to_response()


class UpdateInventoryView(CheckAdminPermissionMixin, StatusWrapMixin, JsonResponseMixin, UpdateView):
    http_method_names = ['post']
    model = GoodsInventory
    pk_url_kwarg = 'iid'

    def post(self, request, *args, **kwargs):
        cost = self.request.POST.get('cost')
        if not cost:
            self.message = '参数缺失'
            self.status_code = ERROR_DATA
            return self.render_to_response()
        obj = self.get_object()
        obj.cost = cost
        obj.save()
        return self.render_to_response({'object': obj})


class UploadPictureView(CheckAdminPermissionMixin, StatusWrapMixin, JsonResponseMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        try:
            from PIL import Image
            img_data = request.FILES.get('image')
            img = Image.open(img_data)
            name = generate_hash(img_data.name, unicode(time.time()))
            img.save('{0}image/{1}.png'.format(STATIC_ROOT, name), "PNG")
            return self.render_to_response({'url': '/static/image/{0}.png'.format(name)})
        except Exception as e:
            logging.exception('ERROR in upload image reason {0}'.format(e))
            self.message = '未知错误'
            self.status_code = ERROR_UNKNOWN
            return self.render_to_response()


class QtRedirctView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect('https://qr.alipay.com/c1x06947u55wqijazkfykb9')

