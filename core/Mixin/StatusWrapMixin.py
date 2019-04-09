# coding: utf-8
from __future__ import unicode_literals

import datetime
import calendar
from django.http import HttpResponse

# Info Code
from drilling.utils import add_timezone_to_naive_time, string_to_datetime

ERROR_UNKNOWN = 0
INFO_SUCCESS = 1
ERROR_PERMISSION_DENIED = 2
ERROR_ACCOUNT_NO_EXIST = 3
ERROR_TOKEN = 3
ERROR_DATA = 4
ERROR_PASSWORD = 5
INFO_EXISTED = 6
INFO_NO_EXIST = 7
INFO_EXPIRE = 8
INFO_NO_VERIFY = 10
ERROR_VERIFY = 11
INFO_NO_MATCH = 20
INFO_ROOM_DESTROY = 21


class StatusWrapMixin(object):
    status_code = INFO_SUCCESS
    message = 'success'

    def render_to_response(self, context={}, **response_kwargs):
        context_dict = self.context_serialize(context)
        json_context = self.json_serializer(self.wrapper(context_dict))
        return HttpResponse(json_context, content_type='application/json', **response_kwargs)

    def wrapper(self, context):
        return_data = dict()
        return_data['body'] = context
        return_data['status'] = self.status_code
        return_data['msg'] = self.message
        if self.status_code != INFO_SUCCESS and self.status_code != INFO_NO_MATCH:
            return_data['body'] = {}
        return return_data


class AdminStatusWrapMixin(StatusWrapMixin):
    def wrapper(self, context):
        data = super(AdminStatusWrapMixin, self).wrapper(context)
        if isinstance(self.message, unicode):
            data['msg'] = {'message': self.message}
            return data
        error_data = {}
        if isinstance(self.message, list):
            for itm in self.message:
                error_data[itm[0]] = itm[1]
        if isinstance(self.message, dict):
            for k, v in self.message.items():
                error_data[k] = v[0].get('message', '')
        data['msg'] = error_data
        return data


class DateTimeHandleMixin(object):
    now = datetime.datetime.now()
    yesterday = now - datetime.timedelta(days=1)
    st_format = {'day': add_timezone_to_naive_time(datetime.datetime(now.year, now.month, now.day)),
                 'stage': add_timezone_to_naive_time(datetime.datetime(now.year, now.month, now.day)),
                 'yesterday': add_timezone_to_naive_time(
                     datetime.datetime(yesterday.year, yesterday.month, yesterday.day)),
                 'week': add_timezone_to_naive_time(now - datetime.timedelta(days=now.weekday())),
                 'last_week': add_timezone_to_naive_time(now - datetime.timedelta(days=now.weekday() + 7)),
                 'month': add_timezone_to_naive_time(datetime.datetime(now.year, now.month, day=1)),
                 'year': add_timezone_to_naive_time(datetime.datetime(now.year, 1, 1)),
                 'last_year': add_timezone_to_naive_time(datetime.datetime(now.year - 1, 1, 1))}
    et_format = {'day': add_timezone_to_naive_time(datetime.datetime(now.year, now.month, now.day, 23, 59, 59)),
                 'yesterday': add_timezone_to_naive_time(
                     datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59)),
                 'week': add_timezone_to_naive_time(now + datetime.timedelta(days=6 - now.weekday())),
                 'last_week': add_timezone_to_naive_time(now - datetime.timedelta(days=now.weekday() + 1)),
                 'month': add_timezone_to_naive_time(
                     datetime.datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], 23, 59, 59)),
                 'year': add_timezone_to_naive_time(datetime.datetime(now.year, 12, 31, 23, 59, 59)),
                 'last_year': add_timezone_to_naive_time(datetime.datetime(now.year - 1, 12, 31, 23, 59, 59))}

    @staticmethod
    def replace_time_to_end(time_obj):
        return time_obj.replace(hour=23, minute=59, second=59)

    @staticmethod
    def replace_time_to_start(time_obj):
        return time_obj.replace(hour=0, minute=0, second=0)

    @staticmethod
    def get_day_stage_time():
        from api.models import InventoryRecord
        ir = InventoryRecord.objects.filter(original_create_time__hour__in=(15, 16, 17)).order_by(
            '-original_create_time').all()
        if ir.exists():
            ir = ir[0]
            return ir.original_create_time
        now = datetime.datetime.now()
        return add_timezone_to_naive_time(datetime.datetime(now.year, now.month, now.day, 23, 59, 59))

    def get_date_period(self, fmt='day', compare=False):
        st = self.request.GET.get('start_time')
        et = self.request.GET.get('end_time')
        if fmt == 'stage':
            st = self.replace_time_to_start(self.st_format.get('day'))
            et = self.replace_time_to_end(self.et_format.get('stage'))
        elif not (st or et):
            st = self.replace_time_to_start(self.st_format.get(fmt))
            et = self.replace_time_to_end(self.et_format.get(fmt))
        else:
            st = string_to_datetime(st)
            et = string_to_datetime(et)
            if compare:
                st, et = self.get_date_period_by_time(st, fmt)
        return st, et

    def get_date_period_by_time(self, time_obj, fmt='day'):
        from dateutil.relativedelta import relativedelta
        now = time_obj
        yesterday = now - datetime.timedelta(days=1)
        last_mon = now - relativedelta(months=1)
        st_format = {'day': add_timezone_to_naive_time(datetime.datetime(now.year, now.month, now.day)),
                     'yesterday': add_timezone_to_naive_time(
                         datetime.datetime(yesterday.year, yesterday.month, yesterday.day)),
                     'week': add_timezone_to_naive_time(now - datetime.timedelta(days=now.weekday())),
                     'last_week': add_timezone_to_naive_time(now - datetime.timedelta(days=now.weekday() + 7)),
                     'month': add_timezone_to_naive_time(datetime.datetime(now.year, now.month, day=1)),
                     'last_month': add_timezone_to_naive_time(datetime.datetime(last_mon.year, last_mon.month, 1)),
                     'year': add_timezone_to_naive_time(datetime.datetime(now.year, 1, 1)),
                     'last_year': add_timezone_to_naive_time(datetime.datetime(now.year - 1, 1, 1))}
        et_format = {'day': add_timezone_to_naive_time(datetime.datetime(now.year, now.month, now.day, 23, 59, 59)),
                     'yesterday': add_timezone_to_naive_time(
                         datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59)),
                     'week': add_timezone_to_naive_time(now + datetime.timedelta(days=6 - now.weekday())),
                     'last_week': add_timezone_to_naive_time(now - datetime.timedelta(days=now.weekday() + 1)),
                     'month': add_timezone_to_naive_time(
                         datetime.datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], 23, 59,
                                           59)),
                     'last_month': add_timezone_to_naive_time(
                         datetime.datetime(now.year, now.month, 1, 23, 59, 59) - datetime.timedelta(days=1)),
                     'year': add_timezone_to_naive_time(datetime.datetime(now.year, 12, 31, 23, 59, 59)),
                     'last_year': add_timezone_to_naive_time(datetime.datetime(now.year - 1, 12, 31, 23, 59, 59))}
        self.now = time_obj
        st = self.replace_time_to_start(st_format.get(fmt))
        et = self.replace_time_to_end(et_format.get(fmt))
        return st, et
