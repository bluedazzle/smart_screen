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
    CardRecord, Excel
from drilling.utils import get_today_st_et, get_week_st_et, add_timezone_to_naive_time
from api.utils import get_fuel_type, get_first_cls_name_by_ss_cls_ids, get_first_cls_name_by_id, get_all_super_cls_id, \
    get_all_goods_super_cls_id, get_card_type


class SmartFinDetailView(DetailView):
    column = None
    ys_column = None
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

    def handle_request(self):
        context = {}
        # context['fuel_type'] = int(self.request.GET.get('fuel_type'))

        context['compare'] = int(self.request.GET.get('compare', 0))
        context['target'] = self.request.GET.get('target', 'month')
        context['year'] = int(self.request.GET.get('year', 0))
        now = datetime.datetime.now()
        if context['target'] == 'month':
            context['st'] = add_timezone_to_naive_time(datetime.datetime(context['year'], 1, 1))
            context['et'] = add_timezone_to_naive_time(datetime.datetime(context['year'], 12, 31))
            context['lst'] = add_timezone_to_naive_time(datetime.datetime(context['year'] - 1, 1, 1))
            context['lst'] = add_timezone_to_naive_time(datetime.datetime(context['year'] - 1, 12, 31))
        else:
            context['st'] = add_timezone_to_naive_time(datetime.datetime(2000, 1, 1))
            context['et'] = add_timezone_to_naive_time(datetime.datetime(now.year, 12, 31))
            context['lst'] = add_timezone_to_naive_time(datetime.datetime(2000, 1, 1))
            context['let'] = add_timezone_to_naive_time(datetime.datetime(now.year, 12, 31))
        return context

    def get_original_time_data(self, context, st, et, belong=None):
        fmt_str, fmt = self.get_time_fmt(st, et)
        belong = self.site.id if not belong else self.site.id
        group_condition = self.model.month if fmt_str == 'month' else self.model.year
        res = session.query(group_condition, self.column).filter(
            self.model.belong_id == belong).group_by(group_condition)
        if fmt_str == 'month':
            res = res.filter(self.model.year == context['year']).all()
        else:
            res = res.all()
        res_dict = {}
        for itm in res:
            res_dict[itm[0]] = itm[1]
        return res_dict

    def get_original_ys_data(self, context, st, et):
        if not self.ys_column:
            return None
        fmt_str, fmt = self.get_time_fmt(st, et)
        group_condition = self.model.month if fmt_str == 'month' else self.model.year
        res = session.query(group_condition, self.ys_column).filter(
            self.model.belong_id == self.site.id).group_by(group_condition)
        if fmt_str == 'month':
            res = res.filter(self.model.year == context['year']).all()
        else:
            res = res.all()
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
            ys = ys.get(k, 0) if ys else 0
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

    def get_data(self, context):
        compare = context['compare']
        target = context['target']
        st = context['start_time']
        et = context['end_time']
        lst = context['last_start_time']
        let = context['last_end_time']
        if compare == 0:
            if target == 'month':
                now = self.get_original_time_data(context, st, et)
                last = self.get_original_time_data(context, lst, let)
                result = self.cal_month_data(now, last)
            else:
                # 预算获取
                ys = self.get_original_ys_data(context, st, et)
                now = self.get_original_time_data(context, st, et)
                # last = self.get_original_time_data(context, lst, let)
                result = self.cal_year_data(now, now, ys)
        else:
            if target == 'month':
                site = self.get_original_time_data(context, st, et)
                comp = self.get_original_time_data(context, st, et, compare)
                result = self.cal_month_comp_site_data(site, comp)
            else:
                site = self.get_original_time_data(context, st, et)
                comp = self.get_original_time_data(context, st, et, compare)
                result = self.cal_year_comp_site_data(site, comp)
        context['object_list'] = result
        return result

    def get(self, request, *args, **kwargs):
        # 计算出月度年度的 st et lst let 到 context
        context = self.handle_request()
        result = self.get_data(context)
        # 处理返回数据单位等
        self.fill_unit(context)
        return self.render_to_response(context)


# 收入指标
# 油品销售数量
class OilSellAmountView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = FuelOrder
    column = FuelOrder.amount
    unit_keys = {'current': '升'}

    fuel_dict = {98: '98号 车用汽油(V)', 95: '95号 车用汽油(Ⅴ)',
                 92: '92号 车用汽油(Ⅴ)', 0: '0号 车用柴油(Ⅴ)',
                 -20: '-20号 车用柴油(Ⅴ)', 35: '35号 车用柴油(Ⅴ)',
                 10: '10号 车用柴油(Ⅴ)', 20: '20号 车用柴油(Ⅴ)'}

    def get_original_time_data(self, context, st, et, belong=None):
        fmt_str, fmt = self.get_time_fmt(st, et)
        belong = self.site.id if not belong else self.site.id
        group_condition = fmt
        res = session.query(group_condition, self.column).filter(
            self.model.fuel_type == self.fuel_dict.get(context.get('fuel_type')),
            self.model.original_create_time.between(st, et),
            self.model.belong_id == belong).group_by(group_condition).all()
        res_dict = {}
        for itm in res:
            res_dict[itm[0]] = itm[1]
        return res_dict


# 油品销售收入
class OilSellMoneyView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = FuelOrder
    column = FuelOrder.total_price
    unit_keys = {'current': '元'}

    fuel_dict = {98: '98号 车用汽油(V)', 95: '95号 车用汽油(Ⅴ)',
                 92: '92号 车用汽油(Ⅴ)', 0: '0号 车用柴油(Ⅴ)',
                 -20: '-20号 车用柴油(Ⅴ)', 35: '35号 车用柴油(Ⅴ)',
                 10: '10号 车用柴油(Ⅴ)', 20: '20号 车用柴油(Ⅴ)'}

    def get_original_time_data(self, context, st, et, belong=None):
        fmt_str, fmt = self.get_time_fmt(st, et)
        belong = self.site.id if not belong else self.site.id
        group_condition = fmt
        res = session.query(group_condition, self.column).filter(
            self.model.fuel_type == self.fuel_dict.get(context.get('fuel_type')),
            self.model.original_create_time.between(st, et),
            self.model.belong_id == belong).group_by(group_condition).all()
        res_dict = {}
        for itm in res:
            res_dict[itm[0]] = itm[1]
        return res_dict


# 非油销售收入
class GoodsSellMoneyView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = GoodsOrder
    column = GoodsOrder.total
    unit_keys = {'current': '元'}

    def get_original_time_data(self, context, st, et, belong=None):
        fmt_str, fmt = self.get_time_fmt(st, et)
        belong = self.site.id if not belong else self.site.id
        group_condition = fmt
        res = session.query(group_condition, self.column).filter(
            self.model.original_create_time.between(st, et),
            self.model.belong_id == belong).group_by(group_condition).all()
        res_dict = {}
        for itm in res:
            res_dict[itm[0]] = itm[1]
        return res_dict


# 成本指标
# 汽油销售成本
class GasSellCostView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.gas_sell_cost_u
    unit_keys = {'current': '元'}


# 柴油销售成本
class DieselSellCostView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.diesel_sell_cost_v
    unit_keys = {'current': '元'}


# 非油销售成本
class GoodsSellCostView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.goods_sell_cost_bi
    unit_keys = {'current': '元'}


# 折旧损耗
class DepreciationCostView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.depreciation_cost_ao
    unit_keys = {'current': '元'}


# 员工薪酬
class SalaryCostView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.salary_cost_ao
    unit_keys = {'current': '元'}


# 日常维修费用
class DailyRepairView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.daily_repair_ad
    unit_keys = {'current': '元'}


# 水电暖费
class WaterEleCostView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.water_ele_cost_af
    unit_keys = {'current': '元'}


# 油品损溢
class OilLossView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.oil_loss_ai
    unit_keys = {'current': '吨'}


# 其他费用
class OtherCostView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.other_cost_aq
    unit_keys = {'current': '元'}


# 费用总额
# todo
class TotalCostView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = [Excel.other_cost_aq, Excel.water_ele_cost_af, Excel.daily_repair_ad, Excel.salary_cost_ao,
              Excel.depreciation_cost_ao, Excel.goods_sell_cost_bi, Excel.gas_sell_cost_u, Excel.diesel_sell_cost_v]

    def get_original_time_data(self, context, st, et, belong=None):
        fmt_str, fmt = self.get_time_fmt(st, et)
        belong = self.site.id if not belong else self.site.id
        group_condition = self.model.month if fmt_str == 'month' else self.model.year
        res = session.query(group_condition, self.column).filter(
            self.model.belong_id == belong).group_by(group_condition)
        if fmt_str == 'month':
            res = res.filter(self.model.year == context['year']).all()
        else:
            res = res.all()
        res_dict = {}
        for itm in res:
            res_dict[itm[0]] = itm[1]
        return res_dict


# 利润指标
# 成品油毛利
class OilGrossProfitView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.oil_gross_profit_w
    unit_keys = {'current': '元'}


# 利润总额
class TotalProfitView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.total_profit_gaddi
    unit_keys = {'current': '元'}


# 成品油利润
class OilProfitView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.oil_profit_g
    unit_keys = {'current': '元'}


# 非油利润
class GoodsProfitView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.goods_profit_i
    unit_keys = {'current': '元'}


# 辅助指标
# 吨油毛利
class TonOilGrossProfitView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.ton_oil_g_profit_wdivn
    unit_keys = {'current': '元'}


# 汽油毛利
class TonGasGrossProfitView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.ton_gas_g_profit_xdivo
    unit_keys = {'current': '元'}


# 汽油毛利
class TonDieselGrossProfitView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.ton_die_g_profit_ydivp
    unit_keys = {'current': '元'}


# 吨油费用
class TonOilCostView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.ton_oil_cost_aadivn
    unit_keys = {'current': '元'}


# 吨油利润
class TonOilProfitView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.ton_oil_profit_j
    unit_keys = {'current': '元'}


# 人均销量
class PerOilAmountView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.per_oil_amount_m
    unit_keys = {'current': '元'}


# 人均利润
# todo
class PerOilProfitView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.per_oil_profit_
    unit_keys = {'current': '元'}


# todo 人均非油


