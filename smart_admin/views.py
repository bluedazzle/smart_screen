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
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.views.generic import View

from SmartScreen.settings import STATIC_ROOT
from drilling.utils import generate_hash
from smart_admin.models import Account
from api.models import GoodsInventory, Site, FuelPlan
from core.Mixin.CheckMixin import CheckAdminPermissionMixin
from core.Mixin.StatusWrapMixin import StatusWrapMixin, INFO_NO_EXIST, ERROR_PASSWORD, ERROR_DATA, ERROR_UNKNOWN, \
    INFO_EXISTED, ERROR_PERMISSION_DENIED
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
    include_attr = ['name', 'slug', 'info', 'pictures', 'lock']

    def get(self, request, *args, **kwargs):
        return self.render_to_response({'site': self.site})

    def post(self, request, *args, **kwargs):
        content = request.POST.get('content')
        pictures = request.POST.get('pictures')
        self.site.info = content
        self.site.pictures = pictures
        self.site.save()
        return self.render_to_response()


class FuelPlanListView(CheckAdminPermissionMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = FuelPlan
    http_method_names = ['get']

    def get_queryset(self):
        queryset = super(FuelPlanListView, self).get_queryset().filter(belong=self.site).order_by('-year')
        return queryset


class FuelPlanView(CheckAdminPermissionMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    model = FuelPlan
    http_method_names = ['post', 'delete']

    def delete(self, request, *args, **kwargs):
        res = FuelPlan.objects.filter(id=kwargs.get('pid'))
        if res.exists():
            res = res[0]
            if res.belong == self.site:
                res.delete()
                return self.render_to_response()
            self.message = '权限不足'
            self.status_code = ERROR_PERMISSION_DENIED
        self.message = '计划不存在'
        self.status_code = INFO_NO_EXIST
        return self.render_to_response()

    def post(self, request, *args, **kwargs):
        # 1 年计划 2 月计划
        plan_type = int(request.POST.get('plan_type', 1))
        # 100101 100102
        fuel_type = int(request.POST.get('fuel_type', 100101))
        total = float(request.POST.get('total', 0))
        jan = float(request.POST.get('jan', 0))
        feb = float(request.POST.get('feb', 0))
        mar = float(request.POST.get('mar', 0))
        apr = float(request.POST.get('apr', 0))
        may = float(request.POST.get('may', 0))
        jun = float(request.POST.get('jun', 0))
        jul = float(request.POST.get('jul', 0))
        aug = float(request.POST.get('aug', 0))
        sep = float(request.POST.get('sep', 0))
        oct = float(request.POST.get('oct', 0))
        nov = float(request.POST.get('nov', 0))
        dec = float(request.POST.get('dec', 0))
        year = int(request.POST.get('year'))
        if fuel_type not in [100101, 100102]:
            self.message = '油品类型不对'
            self.status_code = ERROR_DATA
            return self.render_to_response()
        if not year:
            self.status_code = ERROR_DATA
            self.message = '年份缺失'
            return self.render_to_response()
        res = FuelPlan.objects.filter(year=year, fuel_type_id=fuel_type, belong=self.site).all()
        if res.exists():
            self.status_code = INFO_EXISTED
            self.message = '计划已存在'
            return self.render_to_response()
        fp = FuelPlan(belong=self.site, fuel_type_id=fuel_type, year=year)
        if plan_type == 1:
            month_plan = round(total / 12.0)
            fp.jan = month_plan
            fp.feb = month_plan
            fp.mar = month_plan
            fp.apr = month_plan
            fp.may = month_plan
            fp.jul = month_plan
            fp.jun = month_plan
            fp.aug = month_plan
            fp.sep = month_plan
            fp.nov = month_plan
            fp.dec = month_plan
            fp.oct = month_plan
        else:
            fp.jan = jan
            fp.feb = feb
            fp.mar = mar
            fp.apr = apr
            fp.may = may
            fp.jul = jul
            fp.jun = jun
            fp.aug = aug
            fp.sep = sep
            fp.nov = nov
            fp.dec = dec
            fp.oct = oct
            total = jan + feb + mar + apr + may + jun + jul + aug + sep + oct + nov + dec
        fp.total = total
        fp.save()
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
        # try:
        #     from PIL import Image
        img_data = request.FILES.get('image')
        # img = Image.open(img_data)
        name = generate_hash(img_data.name, unicode(time.time()))
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        default_storage.save('{0}image/{1}.png'.format(STATIC_ROOT, name), ContentFile(img_data.read()))
        # f = open('{0}image/{1}.png'.format(STATIC_ROOT, name), "wb")
        # f.write(img_data)
        # f.close()
        # img.save('{0}image/{1}.png'.formaat(STATIC_ROOT, name), "PNG")
        return self.render_to_response({'url': '/static/image/{0}.png'.format(name)})
        # except Exception as e:
        #     logging.exception('ERROR in upload image reason {0}'.format(e))
        #     self.message = '未知错误'
        #     self.status_code = ERROR_UNKNOWN
        #     return self.render_to_response()


class ExcelUploadView(CheckAdminPermissionMixin, StatusWrapMixin, JsonResponseMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        import xlrd

        file_data = request.FILES.get('excel')
        book = xlrd.open_workbook(file_contents=file_data.read(), encoding_override='utf-8')
        sheet = book.sheet_by_index(0)
        print sheet.row_values(0)
        return self.render_to_response({})