# coding=utf-8
import datetime

import logging
from django.views.generic import DetailView
from django.views.generic import ListView

from sqlalchemy import func

from api import models
from core.Mixin.CheckMixin import CheckSiteMixin
from core.Mixin.StatusWrapMixin import StatusWrapMixin, DateTimeHandleMixin
from core.dss.Mixin import JsonResponseMixin, MultipleJsonResponseMixin
from drilling.models import session, InventoryRecord, FuelOrder, SecondClassification, GoodsOrder, GoodsInventory, \
    CardRecord
from drilling.utils import get_today_st_et, get_week_st_et
from api.utils import get_fuel_type, get_first_cls_name_by_ss_cls_ids, get_first_cls_name_by_id, get_all_super_cls_id, \
    get_all_goods_super_cls_id


class SmartDetailView(DetailView):
    data_keys = []
    display_func = {}
    date_fmt = 'day'
    all_keys = None

    def format_data(self, context, data):
        formated_data = []
        for itm in data:
            body = dict(zip(self.data_keys, itm))
            for k, v in self.display_func.items():
                body[k] = v(body[k])
            formated_data.append(body)
        context['object_list'] = formated_data
        return formated_data

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
        return self.render_to_response(context)


class TankListInfoView(CheckSiteMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = models.FuelTank

    def set_extra(self, obj):
        status = '正常'
        percentage = round(obj.current / float(obj.max_value) * 100, 2)
        if obj.current <= obj.min_value:
            status = '液位过低'
        if obj.current >= obj.max_value:
            status = '液位过高'
        setattr(obj, 'percentage', percentage)
        setattr(obj, 'status', status)

    def get_queryset(self):
        queryset = super(TankListInfoView, self).get_queryset()
        map(self.set_extra, queryset)
        return queryset


class FuelInventoryListView(CheckSiteMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = models.InventoryRecord
    paginate_by = 10


class FuelChargeTimesView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DateTimeHandleMixin, DetailView):
    model = models.InventoryRecord

    def get(self, request, *args, **kwargs):
        st, et = self.get_date_period('month')
        res = session.query(InventoryRecord.fuel_name, func.count('1')).filter(
            InventoryRecord.belong_id == self.site.id,
            InventoryRecord.record_type == 2, InventoryRecord.original_create_time.between(st, et)).group_by(
            InventoryRecord.fuel_name).all()
        res_list = [{'fuel_name': itm[0], 'times': itm[1]} for itm in res]
        return self.render_to_response({'fuel_charges_times': res_list})


class TankerSellTimesView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DateTimeHandleMixin, DetailView):
    model = models.FuelOrder

    def get(self, request, *args, **kwargs):
        st, et = self.get_date_period('day')
        res = session.query(FuelOrder.pump_id, FuelOrder.fuel_type, func.count('1')).filter(
            FuelOrder.belong_id == self.site.id, FuelOrder.original_create_time.between(st, et)).group_by(
            FuelOrder.pump_id, FuelOrder.fuel_type).all()
        res_list = [{'tanker_id': itm[0], 'fuel_name': itm[1], 'times': itm[2]} for itm in res]
        return self.render_to_response({'tanker_sell_times': res_list, 'start_time': st, 'end_time': et})


class FuelOrderPaymentView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DateTimeHandleMixin, DetailView):
    def get(self, request, *args, **kwargs):
        st, et = self.get_date_period()
        res = session.query(FuelOrder.payment_type, func.count('1')).filter(FuelOrder.belong_id == self.site.id,
                                                                            FuelOrder.original_create_time.between(st,
                                                                                                                   et)).group_by(
            FuelOrder.payment_type).all()
        res_list = [{'payment_type': itm[0], 'times': itm[1]} for itm in res]
        return self.render_to_response({'payments': res_list, 'start_time': st, 'end_time': et})


class FuelSequentialView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DateTimeHandleMixin, DetailView):
    """
    油品销售环比
    """

    def get_fuel_type(self, cid):
        obj = session.query(SecondClassification).filter(SecondClassification.id == cid).first()
        return obj.name

    def get(self, request, *args, **kwargs):
        st, et = self.get_date_period('week')
        res = session.query(FuelOrder.super_cls_id, func.count('1')).filter(FuelOrder.belong_id == self.site.id,
                                                                            FuelOrder.original_create_time.between(st,
                                                                                                                   et)).group_by(
            FuelOrder.super_cls_id).all()
        lst, let = self.get_date_period_by_time(st, 'last_week')
        last_res = session.query(FuelOrder.super_cls_id, func.count('1')).filter(FuelOrder.belong_id == self.site.id,
                                                                                 FuelOrder.original_create_time.between(
                                                                                     lst,
                                                                                     let)).group_by(
            FuelOrder.super_cls_id).all()
        res_list = [{'fuel_type': self.get_fuel_type(itm[0]), 'times': itm[1]} for itm in res]
        last_list = [{'fuel_type': self.get_fuel_type(itm[0]), 'times': itm[1]} for itm in last_res]
        context = {'current_data': {'contrast': res_list, 'start_time': st, 'end_time': et},
                   'last_data': {'contrast': last_list, 'start_time': lst, 'end_time': let}}
        return self.render_to_response(context)


class FuelCompareYearView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DateTimeHandleMixin, DetailView):
    """
    油品销售同比
    """

    def get_fuel_type(self, cid):
        obj = session.query(SecondClassification).filter(SecondClassification.id == cid).first()
        return obj.name

    def get(self, request, *args, **kwargs):
        st, et = self.get_date_period('year')
        res = session.query(FuelOrder.super_cls_id, func.date_part('month', FuelOrder.original_create_time),
                            func.count('1')).filter(FuelOrder.belong_id == self.site.id,
                                                    FuelOrder.original_create_time.between(st,
                                                                                           et)).group_by(
            FuelOrder.super_cls_id, func.date_part('month', FuelOrder.original_create_time)).all()
        lst, let = self.get_date_period_by_time(st, 'last_year')
        last_res = session.query(FuelOrder.super_cls_id, func.count('1')).filter(FuelOrder.belong_id == self.site.id,
                                                                                 FuelOrder.original_create_time.between(
                                                                                     lst,
                                                                                     let)).group_by(
            FuelOrder.super_cls_id).all()
        res_list = [{'fuel_type': self.get_fuel_type(itm[0]), 'month': itm[1], 'times': itm[2]} for itm in res]
        last_list = [{'fuel_type': self.get_fuel_type(itm[0]), 'times': itm[1]} for itm in last_res]
        context = {'current_data': {'contrast': res_list, 'start_time': st, 'end_time': et},
                   'last_data': {'contrast': last_list, 'start_time': lst, 'end_time': let}}
        return self.render_to_response(context)


class FuelCompositionView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DateTimeHandleMixin, DetailView):
    """
    油品结构
    """

    def get(self, request, *args, **kwargs):
        st, et = self.get_date_period('week')
        summary_res = session.query(FuelOrder.super_cls_id,
                                    func.count('1')).filter(FuelOrder.belong_id == self.site.id,
                                                            FuelOrder.original_create_time.between(st,
                                                                                                   et)).group_by(
            FuelOrder.super_cls_id).all()
        detail_res = session.query(FuelOrder.fuel_type,
                                   func.count('1')).filter(FuelOrder.belong_id == self.site.id,
                                                           FuelOrder.original_create_time.between(st,
                                                                                                  et)).group_by(
            FuelOrder.fuel_type).all()
        summary_list = [{'fuel_type': get_fuel_type(itm[0]), 'amount': itm[1]} for itm in summary_res]
        detail_list = [{'fuel_type': itm[0], 'amount': itm[1]} for itm in detail_res]
        context = {'summary': summary_list, 'detail': detail_list, 'start_time': st, 'end_time': et}
        return self.render_to_response(context)


class FuelCompareDetailView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DateTimeHandleMixin, SmartDetailView):
    """
    油品销售数据对比
    """
    model = FuelOrder
    data_keys = ['fuel_type', 'hour', 'sales', 'total_price', 'amount']

    def get_objects(self, context):
        st = context['start_time']
        et = context['end_time']
        fmt_str, fmt = self.get_time_fmt(st, et)
        self.data_keys = ['fuel_type', fmt_str, 'sales', 'total_price', 'amount']
        res = session.query(FuelOrder.fuel_type, fmt,
                            func.sum(FuelOrder.amount), func.sum(FuelOrder.total_price), func.count("1")).filter(
            FuelOrder.belong_id == self.site.id, FuelOrder.original_create_time.between(st, et)).group_by(
            FuelOrder.fuel_type, fmt).all()
        return res

    def format_data(self, context, data):
        formated_data = []
        for itm in data:
            body = dict(zip(self.data_keys, itm))
            formated_data.append(body)
        context['object_list'] = formated_data
        return formated_data

    def get(self, request, *args, **kwargs):
        context = {}
        st, et = self.get_date_period()
        context['start_time'] = st
        context['end_time'] = et
        data = self.get_objects(context)
        self.format_data(context, data)
        return self.render_to_response(context)


class GoodsPaymentView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DateTimeHandleMixin, SmartDetailView):
    """
    非油消费类型
    """
    model = GoodsOrder
    data_keys = ['payment_type', 'amount']

    def get_objects(self, context):
        st = context['start_time']
        et = context['end_time']
        res = session.query(self.model.payment_type, func.count("1")).filter(
            self.model.belong_id == self.site.id, self.model.original_create_time.between(st, et)).group_by(
            self.model.payment_type).all()
        return res

    def get(self, request, *args, **kwargs):
        context = {}
        st, et = self.get_date_period()
        context['start_time'] = st
        context['end_time'] = et
        data = self.get_objects(context)
        data = self.format_data(context, data)
        for itm in data:
            cls_list = session.query(self.model.classification_id).filter(
                self.model.belong_id == self.site.id, self.model.payment_type == itm['payment_type'],
                self.model.original_create_time.between(st, et)).all()
            cls_name = get_first_cls_name_by_ss_cls_ids(cls_list)
            itm['cls_name'] = [{"name": cls[0]} for cls in cls_name]
        return self.render_to_response(context)


class GoodsClassificationSellView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DateTimeHandleMixin,
                                  SmartDetailView):
    """
    非油分类销售统计
    """
    model = GoodsOrder
    data_keys = ["cls_name", "amount", 'total_income']
    display_func = {"cls_name": get_first_cls_name_by_id}

    def get_objects(self, context):
        st = context['start_time']
        et = context['end_time']
        res = session.query(self.model.super_cls_id, func.count("1"), func.sum(self.model.total)).filter(
            self.model.belong_id == self.site.id, self.model.original_create_time.between(st, et)).group_by(
            self.model.super_cls_id).all()
        return res


class GoodsSellRankView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DateTimeHandleMixin, SmartDetailView):
    """
    非油销售排行
    """
    model = GoodsOrder
    data_keys = ["name", "amount", "income"]
    date_fmt = 'month'

    def get_objects(self, context):
        st = context['start_time']
        et = context['end_time']
        res = []
        cls_list = session.query(self.model.super_cls_id).filter(
            self.model.belong_id == self.site.id, self.model.original_create_time.between(st, et)).group_by(
            self.model.super_cls_id).order_by(func.count("1").desc()).limit(5).all()
        cls_list = [itm[0] for itm in cls_list]
        for cls in cls_list:
            cls_res = session.query(self.model.name, func.count("1"), func.sum(self.model.total)).filter(
                self.model.belong_id == self.site.id, self.model.super_cls_id == cls,
                self.model.original_create_time.between(st, et)).group_by(
                self.model.name).order_by(func.count("1").desc()).limit(50).all()
            cls_res = self.format_data({}, cls_res)
            body = {'cls_name': get_first_cls_name_by_id(cls), 'data': cls_res}
            res.append(body)
        context['object_list'] = res
        return res

    def get(self, request, *args, **kwargs):
        context = {}
        st, et = self.get_date_period()
        context['start_time'] = st
        context['end_time'] = et
        self.get_objects(context)
        return self.render_to_response(context)


class GoodsGuestUnitPriceView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DateTimeHandleMixin, SmartDetailView):
    """
    非油客单价
    """

    model = GoodsOrder
    data_keys = ["hour", "amount", "income"]

    def get_objects(self, context):
        st = context['start_time']
        et = context['end_time']
        fmt_str, fmt = self.get_time_fmt(st, et)
        self.data_keys = [fmt_str, "amount", "income"]
        res = session.query(fmt, func.count("1"),
                            func.sum(self.model.total)).filter(
            self.model.belong_id == self.site.id, self.model.original_create_time.between(st, et)).group_by(
            fmt).order_by(
            fmt).all()
        return res


class ConversionView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DateTimeHandleMixin, SmartDetailView):
    """
    油非转换率
    """

    model = GoodsOrder
    data_keys = ["hour", "goods_total", "fuel_total", "conversion"]

    def get_objects(self, context):
        st = context['start_time']
        et = context['end_time']
        fmt_str, fmt = self.get_time_fmt(st, et)
        self.data_keys = [fmt_str, "goods_total", "fuel_total", "conversion"]
        goods_res = session.query(fmt, func.count("1")).filter(self.model.belong_id == self.site.id,
                                                               self.model.original_create_time.between(st,
                                                                                                       et)).group_by(
            fmt).order_by(
            fmt).all()
        self.model = FuelOrder
        fmt_str, fmt = self.get_time_fmt(st, et)
        fuel_res = session.query(fmt, func.count("1")).filter(self.model.belong_id == self.site.id,
                                                              self.model.original_create_time.between(st,
                                                                                                      et)).group_by(
            fmt).order_by(
            fmt).all()
        combine = zip(goods_res, fuel_res)
        res = [(itm[0][0], itm[0][1], itm[1][1], itm[0][1] / float(itm[1][1])) for itm in combine]
        return res


class FuelGoodsCompareView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DateTimeHandleMixin, SmartDetailView):
    """
    吨油非油分析
    """

    model = GoodsOrder

    def get_objects(self, context):
        st = context['start_time']
        et = context['end_time']
        fmt_str, fmt = self.get_time_fmt(st, et)
        self.data_keys = [fmt_str, "goods_total_income", "fuel_total_amount", "conversion"]
        goods_res = session.query(fmt, func.sum(self.model.total)).filter(self.model.belong_id == self.site.id,
                                                                          self.model.original_create_time.between(st,
                                                                                                                  et)).group_by(
            fmt).order_by(
            fmt).all()
        self.model = FuelOrder
        fmt_str, fmt = self.get_time_fmt(st, et)
        fuel_res = session.query(fmt, func.sum(self.model.amount)).filter(self.model.belong_id == self.site.id,
                                                                          self.model.original_create_time.between(st,
                                                                                                                  et)).group_by(
            fmt).order_by(
            fmt).all()
        combine = zip(goods_res, fuel_res)
        res = [(itm[0][0], itm[0][1], (itm[1][1] / 1000.0), itm[0][1] / (itm[1][1] / 1000.0)) for itm in combine]
        return res


class GoodsItemView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DateTimeHandleMixin, SmartDetailView):
    """
    商品品效
    """

    model = GoodsOrder

    def get_objects(self, context):
        st = context['start_time']
        et = context['end_time']
        fmt_str, fmt = self.get_time_fmt(st, et)
        self.data_keys = [fmt_str, "income", "product_effect", "item_num"]
        goods_res = session.query(fmt, func.sum(self.model.total)).filter(self.model.belong_id == self.site.id,
                                                                          self.model.original_create_time.between(st,
                                                                                                                  et)).group_by(
            fmt).order_by(
            fmt).all()

        total_item = session.query(GoodsInventory).count()
        res = [(itm[0], itm[1], itm[1] / float(total_item), total_item) for itm in goods_res]
        return res


class GoodsOverView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DateTimeHandleMixin, SmartDetailView):
    """
    非油数据总览
    """
    http_method_names = ['get']
    model = GoodsOrder

    def get(self, request, *args, **kwargs):
        st, et = self.get_date_period(self.date_fmt)
        try:
            total, amount = session.query(func.sum(self.model.total), func.count(1)).filter(
                self.model.belong_id == self.site.id,
                self.model.original_create_time.between(st, et)).all()[0]
        except Exception as e:
            logging.exception('ERROR in good overview reason {0}'.format(e))
            total, amount = 0, 0
        if not amount:
            average = total / float(amount)
        else:
            average = 0
        total_item = session.query(GoodsInventory).count()
        self.model = FuelOrder
        try:
            fuel_volumn, fuel_amount = session.query(func.sum(self.model.amount), func.count(1)).filter(
                self.model.belong_id == self.site.id,
                self.model.original_create_time.between(st,
                                                        et)).all()[0]
        except Exception as e:
            logging.exception('ERROR in goods overview reason {0}'.format(e))
            fuel_volumn, fuel_amount = 0, 0
        fuel_ton = fuel_volumn / 1000.0
        product_effect = total / float(total_item)
        ton_oil_goods = total / fuel_ton
        oil_goods_conversion = '{0}%'.format(round(amount / float(fuel_amount) * 100, 2))
        return self.render_to_response(
            {'total': total, 'amount': amount, 'average': average, 'product_effect': product_effect,
             'ton_oil_goods': ton_oil_goods, 'oil_goods_conversion': oil_goods_conversion})


class GoodSequentialView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DateTimeHandleMixin, SmartDetailView):
    """
    商品环比
    """

    model = GoodsOrder
    data_keys = ["cls_id", "cls_name", "amount", "income"]
    display_func = {"cls_name": get_first_cls_name_by_id}
    date_fmt = 'week'

    def get(self, request, *args, **kwargs):
        context = {}
        st, et = self.get_date_period(self.date_fmt, True)
        goods_res = session.query(self.model.super_cls_id, self.model.super_cls_id, func.count("1"),
                                  func.sum(self.model.total)).filter(
            self.model.belong_id == self.site.id,
            self.model.original_create_time.between(st, et)).group_by(self.model.super_cls_id).order_by(
            self.model.super_cls_id).all()
        goods_res = self.fill_data(goods_res)
        current_data = self.format_data(context, goods_res)
        lst, let = self.get_date_period_by_time(st, 'last_{0}'.format(self.date_fmt))
        last_goods_res = session.query(self.model.super_cls_id, self.model.super_cls_id, func.count("1"),
                                       func.sum(self.model.total)).filter(
            self.model.belong_id == self.site.id,
            self.model.original_create_time.between(lst, let)).group_by(self.model.super_cls_id).order_by(
            self.model.super_cls_id).all()
        last_goods_res = self.fill_data(last_goods_res)
        last_data = self.format_data(context, last_goods_res)
        context = {'current_data': {'start_time': st, 'end_time': et, "object_list": current_data},
                   'last_data': {'start_time': lst, 'end_time': let, 'object_list': last_data}}
        return self.render_to_response(context)


class GoodsCompareYearView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DateTimeHandleMixin, SmartDetailView):
    """
    商品同比
    """

    model = GoodsOrder
    data_keys = ["cls_id", "cls_name", "amount", "income"]
    display_func = {"cls_name": get_first_cls_name_by_id}
    date_fmt = 'year'

    def get(self, request, *args, **kwargs):
        context = {}
        st, et = self.get_date_period(self.date_fmt, True)
        goods_res = session.query(self.model.super_cls_id, self.model.super_cls_id, func.count("1"),
                                  func.sum(self.model.total)).filter(
            self.model.belong_id == self.site.id,
            self.model.original_create_time.between(st, et)).group_by(self.model.super_cls_id).order_by(
            self.model.super_cls_id).all()
        goods_res = self.fill_data(goods_res)
        current_data = self.format_data(context, goods_res)
        lst, let = self.get_date_period_by_time(st, 'last_{0}'.format(self.date_fmt))
        last_goods_res = session.query(self.model.super_cls_id, self.model.super_cls_id, func.count("1"),
                                       func.sum(self.model.total)).filter(
            self.model.belong_id == self.site.id,
            self.model.original_create_time.between(lst, let)).group_by(self.model.super_cls_id).order_by(
            self.model.super_cls_id).all()
        last_goods_res = self.fill_data(last_goods_res)
        last_data = self.format_data(context, last_goods_res)
        context = {'current_data': {'start_time': st, 'end_time': et, "object_list": current_data},
                   'last_data': {'start_time': lst, 'end_time': let, 'object_list': last_data}}
        return self.render_to_response(context)


class GoodsSearchSequentialView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DateTimeHandleMixin,
                                SmartDetailView):
    """
    搜索环比
    """

    model = GoodsOrder
    data_keys = ["name", "amount", "income"]
    date_fmt = 'week'

    def search_goods_by_key(self, key):
        res = session.query(self.model.barcode).filter(self.model.barcode == key).first()
        if res:
            return res[0]
        res = session.query(self.model.barcode).filter(self.model.name == key).first()
        return res[0] if res else None

    def get(self, request, *args, **kwargs):
        key = request.GET.get('search')
        if not key:
            return self.render_to_response()
        barcode = self.search_goods_by_key(key)
        if not barcode:
            return self.render_to_response()
        context = {}
        st, et = self.get_date_period(self.date_fmt, True)
        goods_res = session.query(self.model.name, func.count("1"),
                                  func.sum(self.model.total)).filter(
            self.model.belong_id == self.site.id, self.model.barcode == barcode,
            self.model.original_create_time.between(st, et)).group_by(self.model.name).all()
        current_data = self.format_data(context, goods_res)
        lst, let = self.get_date_period_by_time(st, 'last_{0}'.format(self.date_fmt))
        last_goods_res = session.query(self.model.name, func.count("1"),
                                       func.sum(self.model.total)).filter(
            self.model.belong_id == self.site.id, self.model.barcode == barcode,
            self.model.original_create_time.between(lst, let)).group_by(self.model.name).all()
        last_data = self.format_data(context, last_goods_res)
        context = {'current_data': {'start_time': st, 'end_time': et, "object_list": current_data},
                   'last_data': {'start_time': lst, 'end_time': let, 'object_list': last_data}}
        return self.render_to_response(context)


class GoodsSearchCompareYearView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DateTimeHandleMixin,
                                 SmartDetailView):
    """
    搜索同比
    """

    model = GoodsOrder
    data_keys = ["name", "amount", "income"]
    date_fmt = 'year'

    def search_goods_by_key(self, key):
        res = session.query(self.model.barcode).filter(self.model.barcode == key).first()
        if res:
            return res[0]
        res = session.query(self.model.barcode).filter(self.model.name == key).first()
        return res[0] if res else None

    def get(self, request, *args, **kwargs):
        key = request.GET.get('search')
        if not key:
            return self.render_to_response()
        barcode = self.search_goods_by_key(key)
        if not barcode:
            return self.render_to_response()
        context = {}
        st, et = self.get_date_period(self.date_fmt, True)
        goods_res = session.query(self.model.name, func.count("1"),
                                  func.sum(self.model.total)).filter(
            self.model.belong_id == self.site.id, self.model.barcode == barcode,
            self.model.original_create_time.between(st, et)).group_by(self.model.name).all()
        current_data = self.format_data(context, goods_res)
        lst, let = self.get_date_period_by_time(st, 'last_{0}'.format(self.date_fmt))
        last_goods_res = session.query(self.model.name, func.count("1"),
                                       func.sum(self.model.total)).filter(
            self.model.belong_id == self.site.id, self.model.barcode == barcode,
            self.model.original_create_time.between(lst, let)).group_by(self.model.name).all()
        last_data = self.format_data(context, last_goods_res)
        context = {'current_data': {'start_time': st, 'end_time': et, "object_list": current_data},
                   'last_data': {'start_time': lst, 'end_time': let, 'object_list': last_data}}
        return self.render_to_response(context)


class UnsoldView(CheckSiteMixin, StatusWrapMixin, MultipleJsonResponseMixin, DateTimeHandleMixin, ListView):
    """
    滞销商品
    """

    model = models.GoodsInventory
    paginate_by = 20

    @staticmethod
    def get_day_num(obj):
        now = datetime.datetime.now()
        period = now - obj.last_sell_time
        day = period.days
        setattr(obj, 'unsold_day', day)

    @staticmethod
    def get_unsold_datetime(day_str):
        period = datetime.timedelta(days=int(day_str))
        now = datetime.datetime.now()
        unsold_time = now - period
        return unsold_time

    def get_queryset(self):
        queryset = super(UnsoldView, self).get_queryset()
        unsold_day = self.request.GET.get('unsold_day', None)
        if unsold_day:
            unsold_time = self.get_unsold_datetime(unsold_day)
            queryset = queryset.filter(last_sell_time__gt=unsold_time)
        queryset = queryset.order_by('last_sell_time')
        map(self.get_day_num, queryset)
        return queryset


class FuelSellPredict(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DateTimeHandleMixin, SmartDetailView):
    """
    销售预测
    """

    model = FuelOrder
    date_fmt = 'yesterday'

    # display_func = {"fuel_name": get_fuel_type}

    @staticmethod
    def get_fuel_list(fuels):
        fuel_amounts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for itm in fuels:
            fuel_amounts[int(itm[0])] = itm[2]
        return fuel_amounts

    def get_objects(self, context):
        st = context['start_time']
        et = context['end_time']
        now_hour = datetime.datetime.now().hour
        fmt_str, fmt = self.get_time_fmt(st, et)
        self.data_keys = [fmt_str, "fuel_name", "amount"]
        fuel_types = session.query(self.model.fuel_type).filter(
            self.model.belong_id == self.site.id,
            self.model.original_create_time.between(st,
                                                    et)).group_by(
            self.model.fuel_type).order_by(
            self.model.fuel_type).all()
        fuel_types = [itm[0] for itm in fuel_types]
        fuel_predict_list = []
        for fuel_type in fuel_types:
            body = {}
            last_day_fuels = session.query(fmt, self.model.fuel_type, func.count("1")).filter(
                self.model.belong_id == self.site.id, self.model.fuel_type == fuel_type,
                self.model.original_create_time.between(st,
                                                        et)).group_by(
                fmt, self.model.fuel_type).order_by(
                fmt).all()
            lst = st - datetime.timedelta(days=7)
            let = et - datetime.timedelta(days=7)
            last_seven_day_fuels = session.query(fmt, self.model.fuel_type, func.count("1")).filter(
                self.model.belong_id == self.site.id, self.model.fuel_type == fuel_type,
                self.model.original_create_time.between(lst,
                                                        let)).group_by(
                fmt, self.model.fuel_type).order_by(
                fmt).all()
            last_fuel_list = self.get_fuel_list(last_day_fuels)
            last_seven_fuels_list = self.get_fuel_list(last_seven_day_fuels)
            total_fuel = last_fuel_list + last_seven_fuels_list
            total = reduce(lambda x, y: x + y, total_fuel)
            average = total / float(len(total_fuel))
            combine = zip(last_fuel_list, last_seven_fuels_list)
            predict_list = []
            predict_str = '低峰期'
            is_peak = False
            for i, itm in enumerate(combine):
                ava = (itm[0] + itm[1]) / 2
                if i == now_hour:
                    if ava > average:
                        predict_str = '高峰期'
                        is_peak = True
                itm_dict = {'hour': i, 'amount': ava}
                predict_list.append(itm_dict)
            body['average'] = average
            body['predict_list'] = predict_list
            body['fuel_name'] = fuel_type
            body['predict_str'] = predict_str
            body['is_peak'] = is_peak
            fuel_predict_list.append(body)
        context['fuel_predict_list'] = fuel_predict_list
        return context

    def get(self, request, *args, **kwargs):
        context = {}
        st, et = self.get_date_period(self.date_fmt)
        context['start_time'] = st
        context['end_time'] = et
        data = self.get_objects(context)
        return self.render_to_response(context)


class DayTimeView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, ListView):
    """
    日结时间
    """
    datetime_type = 'string'

    def get(self, request, *args, **kwargs):
        ir = session.query(InventoryRecord).filter(InventoryRecord.record_type == 3).order_by(
            InventoryRecord.original_create_time.desc()).first()
        end_time = ir.original_create_time + datetime.timedelta(days=1)
        return self.render_to_response({'start_time': ir.original_create_time, 'end_time': end_time})


class FuelSellPlanView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DateTimeHandleMixin,
                       SmartDetailView):
    """
    销售计划
    """
    model = FuelOrder
    display_func = {'fuel_type': get_fuel_type}

    def get_plan(self, fmt_str, cls, fmt, st):
        month_dict = {1: 'jan', 2: 'feb', 3: 'mar', 4: 'apr', 5: 'may', 6: 'jun', 7: 'jul', 8: 'aug', 9: 'sep',
                      10: 'oct', 11: 'nov', 12: 'dec'}
        if fmt_str == 'year':
            # month_str = month_dict.get(month)
            # year = datetime.datetime.now().year
            # cls = models.SecondClassification.objects.filter(id=cls)[0]
            plan = models.FuelPlan.objects.filter(year=fmt, fuel_type_id=cls)
            if not plan.exists():
                return 0
            plan = plan[0]
            year_plan_num = plan.total
            return year_plan_num
        if fmt_str == 'month':
            month_str = month_dict.get(fmt)
            year = st.year
            # cls = models.SecondClassification.objects.filter(id=cls)[0]
            plan = models.FuelPlan.objects.filter(year=year, fuel_type_id=cls)
            if not plan.exists():
                return 0
            plan = plan[0]
            month_plan_num = getattr(plan, month_str)
            return month_plan_num
        month_str = month_dict.get(st.month)
        year = st.year
        plan = models.FuelPlan.objects.filter(year=year, fuel_type_id=cls)
        if not plan.exists():
            return 0
        plan = plan[0]
        month_plan_num = getattr(plan, month_str)
        day_plan_num = month_plan_num / 31
        if fmt_str == 'day':
            return day_plan_num
        hour_plan_num = day_plan_num / 24
        if fmt_str == 'hour':
            return hour_plan_num

    def get_objects(self, context):
        st = context['start_time']
        et = context['end_time']
        fmt_str, fmt = self.get_time_fmt(st, et)
        fuel_res = session.query(fmt, self.model.super_cls_id, func.sum(self.model.amount)).filter(
            self.model.belong_id == self.site.id,
            self.model.original_create_time.between(st,
                                                    et)).group_by(
            fmt, self.model.super_cls_id).order_by(
            fmt).all()
        res = []
        for data in fuel_res:
            res.append((data[0], data[1], data[2] / 1000.0, self.get_plan(fmt_str, data[1], data[0], st)))
        self.data_keys = [fmt_str, 'fuel_type', 'sell', 'plan']
        # res = [(itm[0][0], itm[0][1], (itm[1][1] / 1000.0), itm[0][1] / (itm[1][1] / 1000.0)) for itm in combine]
        return res


class CardRecordTypeView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DateTimeHandleMixin,
                         SmartDetailView):
    """
    卡消费结构
    """

    model = CardRecord
    data_keys = ['cls_name', 'amount']

    def get_objects(self, context):
        st = context['start_time']
        et = context['end_time']
        res = session.query(self.model.classification, func.count(1)).filter(
            self.model.belong_id == self.site.id, self.model.original_create_time.between(st, et)).group_by(
            self.model.classification).all()
        return res


class CardRecordCompareView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DateTimeHandleMixin,
                            SmartDetailView):
    """
    卡销比
    """

    model = CardRecord
    data_keys = ['cls_name', 'total_money']

    def get_objects(self, context):
        st = context['start_time']
        et = context['end_time']
        res = session.query(self.model.classification, func.sum(self.model.total)).filter(
            self.model.belong_id == self.site.id, self.model.original_create_time.between(st, et)).group_by(
            self.model.classification).all()
        res = [(itm[0], itm[1] / 100.0) for itm in res]
        return res


class CardRecordListView(CheckSiteMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    """
    卡消费记录
    """

    model = models.CardRecord
    paginate_by = 50
    foreign = True
    exclude_attr = ['belong', 'parent']

    def get_queryset(self):
        search = self.request.GET.get('search', None)
        queryset = super(CardRecordListView, self).get_queryset().order_by('-original_create_time')
        if search:
            queryset = queryset.filter(card_id=search).order_by('-original_create_time')
        return queryset


class AbnormalCardView(CheckSiteMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    """
    异常卡监控
    """

    model = models.AbnormalRecord
    paginate_by = 50

    def get_queryset(self):
        st, et = get_today_st_et()
        queryset = super(AbnormalCardView, self).get_queryset()
        queryset_day = queryset.filter(abnormal_type=1, start_time__gte=st, end_time__gte=et)
        st, et = get_week_st_et()
        queryset_week = queryset.filter(abnormal_type=2, start_time__gte=st, end_time__gte=et)
        queryset = queryset_day | queryset_week
        queryset = queryset.order_by('-create_time')
        return queryset


class CardOverView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DateTimeHandleMixin, SmartDetailView):
    """
    卡数据总览
    """

    model = CardRecord
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        st, et = self.get_date_period(self.date_fmt)
        try:
            total, amount = session.query(func.sum(self.model.total), func.count(1)).filter(
                self.model.original_create_time.between(st, et)).all()[0]
        except Exception as e:
            logging.exception('ERROR in card overview reason {0}'.format(e))
            total, amount = 0, 0
        return self.render_to_response({'income': total, 'amount': amount})


class SiteInfoView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    model = models.Site
    http_method_names = ['get']
    include_attr = ['name', 'slug', 'info']

    def get(self, request, *args, **kwargs):
        return self.render_to_response({'site': self.site})