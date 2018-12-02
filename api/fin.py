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
    CardRecord, Excel, Site
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
    str_dens_list = {0: 0.85, 92: 0.759, 95: 0.77, 98: 0.77}
    api_name = ''
    average = False
    ton = False
    wan = False

    def get_str_dens(self, den_str):
        return self.str_dens_list.get(den_str, 0.85)
        # for k, v in self.str_dens_list.items():
        #     if k in den_str:
        #         return v

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
        self.unit_keys = {'amount': '万元', 'income': '吨'}
        return output

    def get_time_fmt(self, st, et):
        period = et - st
        if period <= datetime.timedelta(days=1):
            return 'hour', None
            # return 'hour'
        elif datetime.timedelta(days=1) < period < datetime.timedelta(days=31):
            # return 'day'
            return 'day', None

        elif period > datetime.timedelta(days=365):
            return 'year', None

        else:
            return 'month', None

            # return 'month'

    def handle_request(self):
        context = {}
        # context['fuel_type'] = int(self.request.GET.get('fuel_type'))

        context['compare'] = int(self.request.GET.get('compare', 0))
        context['target'] = self.request.GET.get('target', 'month')
        context['year'] = int(self.request.GET.get('year', 0))
        now = datetime.datetime.now()
        if context['target'] == 'month':
            context['start_time'] = add_timezone_to_naive_time(datetime.datetime(context['year'], 1, 1))
            context['end_time'] = add_timezone_to_naive_time(datetime.datetime(context['year'], 12, 31))
            context['last_start_time'] = add_timezone_to_naive_time(datetime.datetime(context['year'] - 1, 1, 1))
            context['last_end_time'] = add_timezone_to_naive_time(datetime.datetime(context['year'] - 1, 12, 31))
        else:
            context['start_time'] = add_timezone_to_naive_time(datetime.datetime(2000, 1, 1))
            context['end_time'] = add_timezone_to_naive_time(datetime.datetime(now.year, 12, 31))
            context['last_start_time'] = add_timezone_to_naive_time(datetime.datetime(2000, 1, 1))
            context['last_end_time'] = add_timezone_to_naive_time(datetime.datetime(now.year, 12, 31))
        return context

    def get_from_db(self, belong, group_condition, fmt_str):
        res = session.query(group_condition, self.column).filter(
            self.model.belong_id == belong).group_by(group_condition)
        return res

    def get_original_time_data(self, context, st, et, belong=None):
        fmt_str, fmt = self.get_time_fmt(st, et)
        belong = self.site.id if not belong else belong
        group_condition = self.model.month if fmt_str == 'month' else self.model.year
        res = self.get_from_db(belong, group_condition, fmt_str)
        m = 1
        if fmt_str == 'month':
            res = res.filter(self.model.year == st.year).all()
        else:
            m = session.query(Excel.month).filter(Excel.belong_id == self.site.id).order_by(Excel.year.desc(),
                                                                                            Excel.month.desc()).first()[
                0]
            res = res.filter(self.model.month <= m).all()
        res_dict = {}
        for itm in res:
            if self.average and self.site.members:
                res_dict[itm[0]] = round(itm[1] / self.site.members)
            elif self.ton and fmt_str == 'year':
                res_dict[itm[0]] = round(itm[1] / m)
            else:
                res_dict[itm[0]] = round(itm[1])
        return res_dict

    def get_original_ys_data(self, context, st, et):
        if not self.ys_column:
            return None
        fmt_str, fmt = self.get_time_fmt(st, et)
        ys = getattr(self.site, self.ys_column)

        if fmt_str == 'month':
            res = session.query(Excel.month).filter(Excel.belong_id == self.site.id,
                                                    self.model.year == context['year']).all()
            ys /= 12
        else:
            res = session.query(Excel.year).filter(Excel.belong_id == self.site.id).all()
        res_dict = {}
        for itm in res:
            res_dict[itm[0]] = round(ys)
        return res_dict

    def format_num(self, value):
        if self.wan:
            return round(value / 10000.0, 0)
        return round(value, 0)

    def cal_month_data(self, now, last):
        res = []
        for k, v in now.items():
            tq = last.get(k, 0)
            sy = now.get(k - 1, 0)
            itm_dict = {'month': k, 'current': self.format_num(v), 'tq': self.format_num(tq),
                        'last_month': self.format_num(sy), 'tb': self.format_num(v - tq),
                        'hb': self.format_num(v - sy)}
            res.append(itm_dict)
        sorted(res, key=lambda x: x['month'])
        return res

    def cal_year_data(self, now, last, ys_dict):
        res = []
        for k, v in now.items():
            tq = last.get(k - 1, 0)
            ys = ys_dict.get(k, 0) if ys_dict else 0
            itm_dict = {'year': k, 'current': self.format_num(v), 'tq': self.format_num(tq),
                        'yszj': self.format_num(v - ys), 'tqzj': self.format_num(v - tq),
                        'ys': self.format_num(ys)}
            res.append(itm_dict)
        sorted(res, key=lambda x: x['year'])
        return res

    def cal_month_comp_site_data(self, site, comp):
        res = []
        for k, v in site.items():
            comp_current = comp.get(k, 0)
            itm_dict = {'month': k, 'current': self.format_num(comp_current), 'yddb': self.format_num(v - comp_current)}
            res.append(itm_dict)
        sorted(res, key=lambda x: x['month'])
        return res

    def cal_year_comp_site_data(self, site, comp):
        res = []
        for k, v in site.items():
            comp_current = comp.get(k, 0)
            itm_dict = {'year': k, 'current': self.format_num(comp_current), 'nddb': self.format_num(v - comp_current)}
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
        context['api_name'] = self.api_name
        return self.render_to_response(context)


# 收入指标
# 油品销售数量
class OilSellAmountView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = FuelOrder
    column = FuelOrder.amount
    unit_keys = {'current': '吨'}
    api_name = '油品销售数量'

    fuel_dict = {98: '98号 车用汽油(V)', 95: '95号 车用汽油(Ⅴ)',
                 92: '92号 车用汽油(Ⅴ)', 0: '0号 车用柴油(Ⅴ)',
                 -20: '-20号 车用柴油(Ⅴ)', 35: '35号 车用柴油(Ⅴ)',
                 10: '10号 车用柴油(Ⅴ)', 20: '20号 车用柴油(Ⅴ)'}

    fuel_column_dict = {98: 'gas_98', 95: 'gas_95',
                        92: 'gas_92', 0: 'die_0',
                        -20: 'die_d20', 35: 'die_35',
                        10: 'die_10', 20: 'die_20'}

    def handle_request(self):
        context = super(OilSellAmountView, self).handle_request()
        try:
            context['fuel_type'] = int(self.request.GET.get('fuel_type', 92))
        except Exception as e:
            context['fuel_type'] = 92
        self.ys_column = self.fuel_column_dict.get(context['fuel_type'], 'gas_92')
        return context

    def get_original_time_data(self, context, st, et, belong=None):
        fmt_str, fmt = self.get_time_fmt(st, et)
        belong = self.site.id if not belong else belong
        group_condition = fmt
        res = session.query(group_condition, func.sum(self.model.amount)).filter(
            self.model.fuel_type == self.fuel_dict.get(context.get('fuel_type')).encode('utf-8'),
            self.model.original_create_time.between(st, et),
            self.model.belong_id == belong).group_by(group_condition).all()
        res_dict = {}
        for itm in res:
            res_dict[itm[0]] = itm[1] * self.get_str_dens(context.get('fuel_type')) / 1000.0
        return res_dict

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


# 油品销售收入
class OilSellMoneyView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = FuelOrder
    column = model.total_price
    unit_keys = {'current': '万元'}
    api_name = '油品销售收入'
    wan = True

    fuel_dict = {98: '98号 车用汽油(V)', 95: '95号 车用汽油(Ⅴ)',
                 92: '92号 车用汽油(Ⅴ)', 0: '0号 车用柴油(Ⅴ)',
                 -20: '-20号 车用柴油(Ⅴ)', 35: '35号 车用柴油(Ⅴ)',
                 10: '10号 车用柴油(Ⅴ)', 20: '20号 车用柴油(Ⅴ)'}

    fuel_column_dict = {98: 'gas_98', 95: 'gas_95',
                        92: 'gas_92', 0: 'die_0',
                        -20: 'die_d20', 35: 'die_35',
                        10: 'die_10', 20: 'die_20'}

    def handle_request(self):
        context = super(OilSellMoneyView, self).handle_request()
        try:
            context['fuel_type'] = int(self.request.GET.get('fuel_type', 92))
        except Exception as e:
            context['fuel_type'] = 92
        self.ys_column = self.fuel_column_dict.get(context['fuel_type'], 'gas_92')
        return context

    def get_original_time_data(self, context, st, et, belong=None):
        fmt_str, fmt = self.get_time_fmt(st, et)
        belong = self.site.id if not belong else belong
        group_condition = fmt
        res = session.query(group_condition, func.sum(self.model.total_price)).filter(
            self.model.fuel_type == self.fuel_dict.get(context.get('fuel_type')),
            self.model.original_create_time.between(st, et),
            self.model.belong_id == belong).group_by(group_condition).all()
        res_dict = {}
        for itm in res:
            res_dict[itm[0]] = itm[1]
        return res_dict

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


# 非油销售收入
class GoodsSellMoneyView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = GoodsOrder
    column = model.total
    unit_keys = {'current': '万元'}
    api_name = '非油销售收入'
    wan = True

    def get_original_time_data(self, context, st, et, belong=None):
        fmt_str, fmt = self.get_time_fmt(st, et)
        belong = self.site.id if not belong else belong
        group_condition = fmt
        res = session.query(group_condition, func.sum(self.model.total)).filter(
            self.model.original_create_time.between(st, et),
            self.model.belong_id == belong).group_by(group_condition).all()
        res_dict = {}
        for itm in res:
            res_dict[itm[0]] = itm[1]
        return res_dict

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


# 成本指标
# 汽油销售成本
class GasSellCostView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.gas_sell_cost_u
    unit_keys = {'current': '万元'}
    api_name = '汽油销售成本'
    wan = True

    def get_from_db(self, belong, group_condition, fmt_str):
        res = session.query(group_condition, func.sum(self.model.gas_sell_cost_u)).filter(
            self.model.belong_id == belong).group_by(group_condition)
        return res


# 柴油销售成本
class DieselSellCostView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.diesel_sell_cost_v
    unit_keys = {'current': '万元'}
    api_name = '柴油销售成本'
    wan = True

    def get_from_db(self, belong, group_condition, fmt_str):
        res = session.query(group_condition, func.sum(self.model.diesel_sell_cost_v)).filter(
            self.model.belong_id == belong).group_by(group_condition)
        return res


# 非油销售成本
class GoodsSellCostView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.goods_sell_cost_bi
    unit_keys = {'current': '万元'}
    api_name = '非油销售成本'
    wan = True

    def get_from_db(self, belong, group_condition, fmt_str):
        res = session.query(group_condition, func.sum(self.model.goods_sell_cost_bi)).filter(
            self.model.belong_id == belong).group_by(group_condition)
        return res


# 折旧损耗
class DepreciationCostView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.depreciation_cost_ao
    ys_column = 'depreciation_cost'
    unit_keys = {'current': '万元'}
    api_name = '折旧损耗'
    wan = True

    def get_from_db(self, belong, group_condition, fmt_str):
        res = session.query(group_condition, func.sum(self.model.depreciation_cost_ao)).filter(
            self.model.belong_id == belong).group_by(group_condition)
        return res


# 员工薪酬
class SalaryCostView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.salary_cost_ab
    ys_column = 'salary_cost'
    unit_keys = {'current': '万元'}
    api_name = '员工薪酬'
    wan = True

    def get_from_db(self, belong, group_condition, fmt_str):
        res = session.query(group_condition, func.sum(self.model.salary_cost_ab)).filter(
            self.model.belong_id == belong).group_by(group_condition)
        return res


# 日常维修费用
class DailyRepairView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.daily_repair_ad
    ys_column = 'daily_repair'
    unit_keys = {'current': '万元'}
    api_name = '日常维修费用'
    wan = True

    def get_from_db(self, belong, group_condition, fmt_str):
        res = session.query(group_condition, func.sum(self.model.daily_repair_ad)).filter(
            self.model.belong_id == belong).group_by(group_condition)
        return res


# 水电暖费
class WaterEleCostView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.water_ele_cost_af
    ys_column = 'water_ele_cost'
    unit_keys = {'current': '万元'}
    api_name = '水电暖费'
    wan = True

    def get_from_db(self, belong, group_condition, fmt_str):
        res = session.query(group_condition, func.sum(self.model.water_ele_cost_af)).filter(
            self.model.belong_id == belong).group_by(group_condition)
        return res


# 油品损溢
class OilLossView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.oil_loss_ai
    unit_keys = {'current': '万元'}
    api_name = '油品损溢'
    wan = True

    def get_from_db(self, belong, group_condition, fmt_str):
        res = session.query(group_condition, func.sum(self.model.oil_loss_ai)).filter(
            self.model.belong_id == belong).group_by(group_condition)
        return res


# 其他费用
class OtherCostView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.other_cost_aq
    ys_column = 'other_cost'
    unit_keys = {'current': '万元'}
    api_name = '其他费用'
    wan = True

    #
    # def get_from_db(self, belong, group_condition, fmt_str):
    #     res = session.query(group_condition, func.sum(self.model.other_cost_aq)).filter(
    #         self.model.belong_id == belong).group_by(group_condition)
    #     return res

    def get_original_time_data(self, context, st, et, belong=None):
        fmt_str, fmt = self.get_time_fmt(st, et)
        belong = self.site.id if not belong else belong
        group_condition = self.model.month if fmt_str == 'month' else self.model.year
        res = session.query(group_condition,
                            func.sum(
                                Excel.total_cost_aa - Excel.water_ele_cost_af - Excel.daily_repair_ad - Excel.salary_cost_ab -
                                Excel.depreciation_cost_ao - Excel.oil_loss_ai)).filter(
            self.model.belong_id == belong).group_by(group_condition)
        m = 1
        if fmt_str == 'month':
            res = res.filter(self.model.year == st.year).all()
        else:
            m = session.query(Excel.month).filter(Excel.belong_id == self.site.id).order_by(Excel.year.desc(),
                                                                                            Excel.month.desc()).first()[
                0]
            res = res.filter(self.model.month <= m).all()
        res_dict = {}
        for itm in res:
            res_dict[itm[0]] = round(itm[1])
        return res_dict


# 费用总额
class TotalCostView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    # column = [Excel.other_cost_aq, Excel.water_ele_cost_af, Excel.daily_repair_ad, Excel.salary_cost_ab,
    #           Excel.depreciation_cost_ao, Excel.goods_sell_cost_bi, Excel.gas_sell_cost_u, Excel.diesel_sell_cost_v]
    column = Excel.total_cost_aa
    api_name = '费用总额'
    ys_column = 'total_cost'
    unit_keys = {'current': '万元'}
    wan = True

    def get_from_db(self, belong, group_condition, fmt_str):
        res = session.query(group_condition, func.sum(self.model.total_cost_aa)).filter(
            self.model.belong_id == belong).group_by(group_condition)
        return res

        # def get_original_time_data(self, context, st, et, belong=None):
        #     fmt_str, fmt = self.get_time_fmt(st, et)
        #     belong = self.site.id if not belong else self.site.id
        #     group_condition = self.model.month if fmt_str == 'month' else self.model.year
        #     res = session.query(group_condition,
        #                         func.sum(
        #                             Excel.other_cost_aq + Excel.water_ele_cost_af + Excel.daily_repair_ad + Excel.salary_cost_ab +
        #                             Excel.depreciation_cost_ao + Excel.goods_sell_cost_bi + Excel.gas_sell_cost_u + Excel.diesel_sell_cost_v)).filter(
        #         self.model.belong_id == belong).group_by(group_condition)
        #     if fmt_str == 'month':
        #         res = res.filter(self.model.year == context['year']).all()
        #     else:
        #         res = res.all()
        #     res_dict = {}
        #     for itm in res:
        #         res_dict[itm[0]] = itm[1]
        #     return res_dict


# 利润指标
# 成品油成品油毛利
class OilGrossProfitView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.oil_gross_profit_w
    ys_column = 'oil_gross_profit'
    unit_keys = {'current': '万元'}
    wan = True
    api_name = '成品油毛利'

    def get_from_db(self, belong, group_condition, fmt_str):
        res = session.query(group_condition, func.sum(self.model.oil_gross_profit_w)).filter(
            self.model.belong_id == belong).group_by(group_condition)
        return res


# 利润总额
class TotalProfitView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.total_profit_f
    ys_column = 'total_profit'
    unit_keys = {'current': '万元'}
    wan = True
    api_name = '利润总额'

    def get_from_db(self, belong, group_condition, fmt_str):
        res = session.query(group_condition, func.sum(self.model.total_profit_f)).filter(
            self.model.belong_id == belong).group_by(group_condition)
        return res


# 成品油利润
class OilProfitView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.oil_profit_g
    ys_column = 'oil_profit'
    unit_keys = {'current': '万元'}
    wan = True
    api_name = '成品油利润'

    def get_from_db(self, belong, group_condition, fmt_str):
        res = session.query(group_condition, func.sum(self.model.oil_profit_g)).filter(
            self.model.belong_id == belong).group_by(group_condition)
        return res


# 非油利润
class GoodsProfitView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.goods_profit_i
    ys_column = 'goods_profit'
    unit_keys = {'current': '万元'}
    wan = True
    api_name = '非油利润'

    def get_from_db(self, belong, group_condition, fmt_str):
        res = session.query(group_condition, func.sum(self.model.goods_profit_i)).filter(
            self.model.belong_id == belong).group_by(group_condition)
        return res


# 辅助指标
# 吨油毛利
class TonOilGrossProfitView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.oil_gross_profit_w
    ys_column = 'ton_oil_g_profit'
    unit_keys = {'current': '元/吨'}
    # wan = True
    api_name = '吨油毛利'

    # ton = True

    def get_from_db(self, belong, group_condition, fmt_str):
        res = session.query(group_condition,
                            func.sum(self.model.oil_gross_profit_w) / func.sum(self.model.oil_amount_n)).filter(
            self.model.belong_id == belong).group_by(group_condition)
        return res


# 汽油毛利
class TonGasGrossProfitView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = [Excel.base_x, Excel.base_o]
    unit_keys = {'current': '元/吨'}
    # wan = True
    api_name = '汽油毛利'

    # ton = True

    def get_from_db(self, belong, group_condition, fmt_str):
        res = session.query(group_condition, func.sum(self.model.base_x) / func.sum(self.model.base_o)).filter(
            self.model.belong_id == belong).group_by(group_condition)
        return res


# 柴油毛利
class TonDieselGrossProfitView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = [Excel.base_y, Excel.base_p]
    unit_keys = {'current': '元/吨'}
    # wan = True
    api_name = '柴油毛利'

    # ton = True

    def get_from_db(self, belong, group_condition, fmt_str):
        res = session.query(group_condition, func.sum(self.model.base_y) / func.sum(self.model.base_p)).filter(
            self.model.belong_id == belong).group_by(group_condition)
        return res


# 吨油费用
class TonOilCostView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = [Excel.total_cost_aa, Excel.oil_amount_n]
    ys_column = 'ton_oil_cost'
    unit_keys = {'current': '元/吨'}
    # wan = True
    api_name = '吨油费用'

    # ton = True

    def get_from_db(self, belong, group_condition, fmt_str):
        res = session.query(group_condition,
                            func.sum(self.model.total_cost_aa) / func.sum(self.model.oil_amount_n)).filter(
            self.model.belong_id == belong).group_by(group_condition)
        return res


# 吨油利润
class TonOilProfitView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = [Excel.total_profit_f, Excel.oil_amount_n]
    unit_keys = {'current': '元/吨'}
    # wan = True
    api_name = '吨油利润'

    # ton = True

    def get_from_db(self, belong, group_condition, fmt_str):
        res = session.query(group_condition,
                            func.sum(self.model.total_profit_f) / func.sum(self.model.oil_amount_n)).filter(
            self.model.belong_id == belong).group_by(group_condition)
        return res


# 人均销量
class PerOilAmountView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.oil_amount_n
    ys_column = 'per_oil_amount'
    unit_keys = {'current': '吨'}
    api_name = '人均销量'
    average = True

    def get_from_db(self, belong, group_condition, fmt_str):
        res = session.query(group_condition, func.sum(self.model.oil_amount_n)).filter(
            self.model.belong_id == belong).group_by(group_condition)
        return res


# 人均利润
class PerOilProfitView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.total_profit_f
    ys_column = 'per_profit'
    average = True
    unit_keys = {'current': '万元'}
    wan = True
    api_name = '人均利润'

    def get_from_db(self, belong, group_condition, fmt_str):
        res = session.query(group_condition, func.sum(self.model.total_profit_f)).filter(
            self.model.belong_id == belong).group_by(group_condition)
        return res


# 人均非油收入
class PerGoodsProfitView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.total_goods_profit_bh
    ys_column = 'per_profit'
    average = True
    wan = True
    unit_keys = {'current': '万元'}
    api_name = '人均非油收入'

    def get_from_db(self, belong, group_condition, fmt_str):
        res = session.query(group_condition, func.sum(self.model.total_goods_profit_bh)).filter(
            self.model.belong_id == belong).group_by(group_condition)
        return res


# class PerGoodsProfitView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
#     model = GoodsOrder
#     column = GoodsOrder.total
#     ys_column = 'per_goods_income'
#     unit_keys = {'current': '万元'}
#     average = True
#     api_name = '人均非油收入'
#
#     def get_original_time_data(self, context, st, et, belong=None):
#         fmt_str, fmt = self.get_time_fmt(st, et)
#         belong = self.site.id if not belong else self.site.id
#         group_condition = fmt
#         res = session.query(group_condition, func.sum(self.model.total)).filter(
#             self.model.original_create_time.between(st, et),
#             self.model.belong_id == belong).group_by(group_condition).all()
#         res_dict = {}
#         for itm in res:
#             if self.average and self.site.members:
#                 res_dict[itm[0]] = itm[1] / self.site.members
#             else:
#                 res_dict[itm[0]] = itm[1]
#         return res_dict
#
#     def get_time_fmt(self, st, et):
#         period = et - st
#         if period <= datetime.timedelta(days=1):
#             return 'hour', func.date_part('hour', self.model.original_create_time)
#             # return 'hour'
#         elif datetime.timedelta(days=1) < period < datetime.timedelta(days=31):
#             # return 'day'
#             return 'day', func.date_part('day', self.model.original_create_time)
#
#         elif period > datetime.timedelta(days=365):
#             return 'year', func.date_part('year', self.model.original_create_time)
#
#         else:
#             return 'month', func.date_part('month', self.model.original_create_time)


# 单站日销量
class DailySellAmountView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.oil_amount_n
    unit_keys = {'current': '吨'}
    api_name = '单站日销量'

    def get_from_db(self, belong, group_condition, fmt_str):
        res = session.query(group_condition, func.sum(self.model.oil_amount_n)).filter(
            self.model.belong_id == belong).group_by(group_condition)
        return res

    def get_original_time_data(self, context, st, et, belong=None):
        fmt_str, fmt = self.get_time_fmt(st, et)
        belong = self.site.id if not belong else belong
        group_condition = self.model.month if fmt_str == 'month' else self.model.year
        res = self.get_from_db(belong, group_condition, fmt_str)
        m = 1
        if fmt_str == 'month':
            res = res.filter(self.model.year == st.year).all()
        else:
            m = session.query(Excel.month).filter(Excel.belong_id == self.site.id).order_by(Excel.year.desc(),
                                                                                            Excel.month.desc()).first()[
                0]
            res = res.filter(self.model.month <= m).all()
        res_dict = {}
        for itm in res:
            if fmt_str == 'year':
                if m == 12:
                    d = 365
                else:
                    d = m * 31
                res_dict[itm[0]] = round(itm[1] / d)
            else:
                res_dict[itm[0]] = round(itm[1] / 31)
        return res_dict


# 单店日均非油收入
class DailyAverageGoodsMoney(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    model = Excel
    column = Excel.total_goods_profit_bh
    unit_keys = {'current': '万元'}
    wan = True
    api_name = '单店日均非油收入'

    def get_from_db(self, belong, group_condition, fmt_str):
        res = session.query(group_condition, func.sum(self.model.total_goods_profit_bh)).filter(
            self.model.belong_id == belong).group_by(group_condition)
        return res

    def get_original_time_data(self, context, st, et, belong=None):
        fmt_str, fmt = self.get_time_fmt(st, et)
        belong = self.site.id if not belong else belong
        group_condition = self.model.month if fmt_str == 'month' else self.model.year
        res = self.get_from_db(belong, group_condition, fmt_str)
        m = 1
        if fmt_str == 'month':
            res = res.filter(self.model.year == st.year).all()
        else:
            m = session.query(Excel.month).filter(Excel.belong_id == self.site.id).order_by(Excel.year.desc(),
                                                                                            Excel.month.desc()).first()[
                0]
            res = res.filter(self.model.month <= m).all()
        res_dict = {}
        for itm in res:
            if fmt_str == 'year':
                res_dict[itm[0]] = round(itm[1] / self.site.open_time)
            else:
                res_dict[itm[0]] = round(itm[1] / 31)
        return res_dict

        # def get_original_time_data(self, context, st, et, belong=None):
        #     fmt_str, fmt = self.get_time_fmt(st, et)
        #     belong = self.site.id if not belong else self.site.id
        #     group_condition = fmt
        #     res = session.query(group_condition, self.column).filter(
        #         self.model.original_create_time.between(st, et),
        #         self.model.belong_id == belong).group_by(group_condition).all()
        #     res_dict = {}
        #     for itm in res:
        #         res_dict[itm[0]] = itm[1]
        #     return res_dict
        #
        # def get_time_fmt(self, st, et):
        #     period = et - st
        #     if period <= datetime.timedelta(days=1):
        #         return 'hour', func.date_part('hour', self.model.original_create_time)
        #         # return 'hour'
        #     elif datetime.timedelta(days=1) < period < datetime.timedelta(days=31):
        #         # return 'day'
        #         return 'day', func.date_part('day', self.model.original_create_time)
        #
        #     elif period > datetime.timedelta(days=365):
        #         return 'year', func.date_part('year', self.model.original_create_time)
        #
        #     else:
        #         return 'month', func.date_part('month', self.model.original_create_time)
        #
        #         # return 'month'


# 盈亏平衡点
class BalanceView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, SmartFinDetailView):
    api_name = '盈亏平衡点'

    def get(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        year = now.year
        total_cost = \
            session.query(func.sum(Excel.total_cost_aa)).filter(
                Excel.belong_id == self.site.id, Excel.year == year).first()[0]
        oil_gross_p = \
            session.query(func.sum(Excel.oil_gross_profit_w)).filter(Excel.belong_id == self.site.id,
                                                                     Excel.year == year).first()[
                0]
        oil_amount = \
            session.query(func.sum(Excel.oil_amount_n)).filter(Excel.belong_id == self.site.id,
                                                               Excel.year == year).first()[
                0]
        return self.render_to_response(
            {'balance': round(total_cost / (oil_gross_p / oil_amount)), 'api_name': self.api_name,
             'advice': self.site.advice,
             'cost_control': self.site.cost_control, 'promote': self.site.promote})


# 对标站
class CompareListView(CheckSiteMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    api_name = '对标站'
    model = models.Site
    include_attr = ['id', 'name', 'slug']

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset
