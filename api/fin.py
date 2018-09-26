# coding=utf-8
from __future__ import unicode_literals
import datetime

import logging

from django.http import HttpResponseRedirect
from django.utils.http import cookie_date
from django.views.generic import DetailView
from django.views.generic import ListView

from sqlalchemy import func

from api import models
from core.Mixin.CheckMixin import CheckSiteMixin
from core.Mixin.StatusWrapMixin import StatusWrapMixin, DateTimeHandleMixin, ERROR_PASSWORD
from core.dss.Mixin import JsonResponseMixin, MultipleJsonResponseMixin, RespCacheMixin
from drilling.models import session, InventoryRecord, FuelOrder, SecondClassification, GoodsOrder, GoodsInventory, \
    CardRecord
from drilling.utils import get_today_st_et, get_week_st_et, add_timezone_to_naive_time
from api.utils import get_fuel_type, get_first_cls_name_by_ss_cls_ids, get_first_cls_name_by_id, get_all_super_cls_id, \
    get_all_goods_super_cls_id, get_card_type


class SmartDetailView(DetailView):
    data_keys = []
    display_func = {}
    date_fmt = 'day'
    all_keys = None
    unit_keys = {}
    dens_list = {100101: 0.770, 100102: 0.85}
    str_dens_list = {'柴油': 0.85, '92': 0.759, '95': 0.77, '98': 0.77}

    def get_str_dens(self, den_str):
        for k, v in self.str_dens_list.items():
            if k in den_str:
                return v

    def format_data(self, context, data):
        formated_data = []
        for itm in data:
            body = dict(zip(self.data_keys, itm))
            for k, v in self.display_func.items():
                body[k] = v(body[k])
            formated_data.append(body)
        context['object_list'] = formated_data
        return formated_data

    def fill_unit(self, context):
        unit_dict = {}
        for k, v in self.unit_keys.items():
            unit_dict['{0}_unit'.format(k)] = v
        context['unit'] = unit_dict

    def fill_data(self, data):
        keys = [itm[0] for itm in data]
        if not self.all_keys:
            self.all_keys = get_all_goods_super_cls_id()
        for key in self.all_keys:
            if key not in keys:
                data.append((key, key) + (0,) * (len(self.data_keys) - 2))
        data = filter(lambda x: 2000 <= x[0] <= 2999, data)
        data = sorted(data, key=lambda x: x[0])
        return data

    def fill_fuel_data(self, data):
        keys = [itm[0] for itm in data]
        self.all_keys = ['98号 车用汽油(V)', '95号 车用汽油(Ⅴ)', '92号 车用汽油(Ⅴ)', '0号 车用柴油(Ⅴ)', '-20号 车用柴油(Ⅴ)', '35号 车用柴油(Ⅴ)',
                         '10号 车用柴油(Ⅴ)', '20号 车用柴油(Ⅴ)']
        for key in self.all_keys:
            if key not in keys:
                data.append((key,) + (0,) * (len(self.data_keys) - 1))
        data = sorted(data, key=lambda x: x[0])
        return data

    def convert_fuel_data(self, data, fmt):
        if fmt == 'hour':
            return data
        output = []
        for itm in data:
            output.append((itm[0], itm[1] * self.get_str_dens(itm[0]) / 1000.0, itm[2]))
        self.unit_keys = {'amount': '元', 'income': '吨'}
        return output

    def get_time_fmt(self, st, et):
        period = et - st
        if period <= datetime.timedelta(days=1):
            return 'hour', func.date_part('hour', self.model.original_create_time)
            # return 'hour'
        elif datetime.timedelta(days=1) < period < datetime.timedelta(days=31):
            # return 'day'
            return 'day', func.date_part('day', self.model.original_create_time)

        elif period > datetime.timedelta(days=365):
            return 'year', func.date_part('year', self.model.original_create_time)

        else:
            return 'month', func.date_part('month', self.model.original_create_time)

            # return 'month'

    def get(self, request, *args, **kwargs):
        context = {}
        st, et = self.get_date_period(self.date_fmt)
        context['start_time'] = st
        context['end_time'] = et
        data = self.get_objects(context)
        self.format_data(context, data)
        self.fill_unit(context)
        return self.render_to_response(context)


class OilSellAmountView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DateTimeHandleMixin, SmartDetailView):
    fuel_dict = {98: '98号 车用汽油(V)', 95: '95号 车用汽油(Ⅴ)',
                 92: '92号 车用汽油(Ⅴ)', 0: '0号 车用柴油(Ⅴ)',
                 -20: '-20号 车用柴油(Ⅴ)', 35: '35号 车用柴油(Ⅴ)',
                 10: '10号 车用柴油(Ⅴ)', 20: '20号 车用柴油(Ⅴ)'}

    def get_original_time_data(self, context, st, et, belong=None):
        fmt_str, fmt = self.get_time_fmt(st, et)
        belong = self.site.id if not belong
        res = session.query(fmt, amount).filter(FuelOrder.fuel_type == self.fuel_dict.get(context.get('fuel_type')),
                                                FuelOrder.original_create_time.between(st, et),
                                                FuelOrder.belong_id == belong).group_by(fmt).all()
        res_dict = {}
        for itm in res:
            res_dict[itm[0]] = itm[1]
        return res_dict

    @staticmethod
    def cal_month_data(now, last):
        res = []
        for k, v in now:
            tq = last.get(k, 0)
            sy = now.get(k - 1, 0)
            itm_dict = {'month': k, 'current': v, 'tq': tq, 'last_month': sy, 'tb': v - tq, 'hb': v - sy}
            res.append(itm_dict)
        sorted(res, key=lambda x: x['month'])
        return res

    @staticmethod
    def cal_year_data(now, last, ys):
        res = []
        for k, v in now:
            tq = last.get(k - 1, 0)
            ys = ys.get(k, 0)
            itm_dict = {'year': k, 'current': v, 'tq': tq, 'yszj': v - ys, 'tqzj': v - tq}
            res.append(itm_dict)
        sorted(res, key=lambda x: x['year'])
        return res

    @staticmethod
    def cal_month_comp_site_data(site, comp):
        res = []
        for k, v in site:
            comp_current = comp.get(k, 0)
            itm_dict = {'month': k, 'current': comp_current, 'yddb': v - comp_current}
            res.append(itm_dict)
        sorted(res, key=lambda x: x['month'])
        return res

    @staticmethod
    def cal_year_comp_site_data(site, comp):
        res = []
        for k, v in site:
            comp_current = comp.get(k, 0)
            itm_dict = {'year': k, 'current': comp_current, 'nddb': v - comp_current}
            res.append(itm_dict)
        sorted(res, key=lambda x: x['year'])
        return res

    def get(self, request, *args, **kwargs):
        context = {}
        # todo  计算出月度年度的 st et lst let 到 context
        context['fuel_type'] = int(request.GET.get('fuel_type'))
        compare = int(request.GET.get('compare', 0))
        target = request.GET.get('target', 'month')
        st = context['start_time']
        et = context['end_time']
        lst = context['last_start_time']
        let = context['last_end_time']
        year = context['year']
        result = None
        if compare == 0:
            if target == 'month':
                now = self.get_original_time_data(context, st, et)
                last = self.get_original_time_data(context, lst, let)
                result = self.cal_month_data(now, last)
            else:
                # todo 预算获取
                ys = None
                now = self.get_original_time_data(context, st, et)
                last = self.get_original_time_data(context, lst, let)
                result = self.cal_year_data(now, last, ys)
        else:
            if target == 'month':
                site = self.get_original_time_data(context, st, et)
                comp = self.get_original_time_data(context, st, et, compare)
                result = self.cal_month_comp_site_data(site, comp)
            else:
                site = self.get_original_time_data(context, st, et)
                comp = self.get_original_time_data(context, st, et, compare)
                result = self.cal_year_comp_site_data(site, comp)

        # todo  处理返回数据单位等
        return self.render_to_response(result)
