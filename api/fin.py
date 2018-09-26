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


class 