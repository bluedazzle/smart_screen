from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView
from django.views.generic import ListView

from drilling.utils import string_to_datetime
from sqlalchemy import func

from core.Mixin.StatusWrapMixin import StatusWrapMixin, DateTimeHandleMixin
from core.Mixin.CheckMixin import CheckSiteMixin
from core.dss.Mixin import JsonResponseMixin, MultipleJsonResponseMixin
from api import models
from drilling.models import session, InventoryRecord, FuelOrder


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
        FuelOrder.original_create_time.between(st, et)).group_by(FuelOrder.payment_type).all()
        res_list = [{'payment_type': itm[0], 'times': itm[1]} for itm in res]
        return self.render_to_response({'payments': res_list, 'start_time': st, 'end_time': et})
