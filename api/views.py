# coding=utf-8
import datetime
from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView
from django.views.generic import ListView

from api.utils import get_fuel_type, get_first_cls_name_by_ss_cls_ids
from drilling.utils import string_to_datetime
from sqlalchemy import func

from core.Mixin.StatusWrapMixin import StatusWrapMixin, DateTimeHandleMixin
from core.Mixin.CheckMixin import CheckSiteMixin
from core.dss.Mixin import JsonResponseMixin, MultipleJsonResponseMixin
from api import models
from drilling.models import session, InventoryRecord, FuelOrder, SecondClassification, GoodsOrder


class SmartDetailView(DetailView):
    data_keys = []

    def format_data(self, context, data):
        formated_data = []
        for itm in data:
            body = dict(zip(self.data_keys, itm))
            formated_data.append(body)
        context['object_list'] = formated_data
        return formated_data

    def get_objects(self, context):
        pass

    def get(self, request, *args, **kwargs):
        context = {}
        st, et = self.get_date_period()
        context['start_time'] = st
        context['end_time'] = et
        data = self.get_objects(context)
        self.format_data(context, data)
        return self.render_to_response(context)


class TankListInfoView(CheckSiteMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = models.FuelTank


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
    data_keys = ['fuel_type', 'hour', 'sales', 'total_price', 'amount']

    def get_objects(self, context):
        st = context['start_time']
        et = context['end_time']
        res = session.query(FuelOrder.fuel_type, func.date_part('hour', FuelOrder.original_create_time),
                            func.sum(FuelOrder.amount), func.sum(FuelOrder.total_price), func.count("1")).filter(
            FuelOrder.belong_id == self.site.id, FuelOrder.original_create_time.between(st, et)).group_by(
            FuelOrder.fuel_type, func.date_part('hour', FuelOrder.original_create_time)).all()
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
