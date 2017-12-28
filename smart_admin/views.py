# coding: utf-8
from __future__ import unicode_literals

# Create your views here.
import random
import string

from django.views.generic import DetailView
from django.views.generic import ListView

from smart_admin.models import Account
from api.models import GoodsInventory, Site
from core.Mixin.CheckMixin import CheckAdminPermissionMixin
from core.Mixin.StatusWrapMixin import StatusWrapMixin, INFO_NO_EXIST, ERROR_PASSWORD
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