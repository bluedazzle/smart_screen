# coding: utf-8
from __future__ import unicode_literals

import datetime

from drilling.fuels import get_sup, get_rev, get_delivery, get_fuel_order
from drilling.models import session, Site
from drilling.store import get_first_classify, get_second_classify, get_third_classify, get_inventories, get_store_order
from drilling.tanks import get_tank_info, get_tank_value, get_tank_temperature, get_tank_grade, get_inventory_record
from drilling.utils import add_timezone_to_naive_time


def init_base_info(site):
    get_tank_info(site)
    get_tank_value(site)
    get_tank_temperature(site)
    get_tank_grade(site)
    print '{0}： 成功获取油罐信息'.format(site)

    get_sup(site)
    get_rev(site)
    print '{0}: 成功获取运送基本信息'.format(site)

    get_first_classify(site)
    get_second_classify(site)
    get_third_classify(site)
    print '{0}: 成功获取分类基本信息'.format(site)

    get_inventories(site)
    print '{0}: 成功获取库存基本信息'.format(site)


def init_day_record(site, st, et):
    get_inventory_record(site, st, et)
    print '{0}: 成功获取{1: %Y-%m-%d}~{2: %Y-%m-%d}油库记录'.format(site, st, et)
    get_delivery(site, st, et)
    print '{0}: 成功获取{1: %Y-%m-%d}~{2: %Y-%m-%d}送货记录'.format(site, st, et)
    get_fuel_order(site, st, et)
    print '{0}: 成功获取{1: %Y-%m-%d}~{2: %Y-%m-%d}油品订单'.format(site, st, et)
    get_store_order(site, st, et)
    print '{0}: 成功获取{1: %Y-%m-%d}~{2: %Y-%m-%d}非油订单'.format(site, st, et)


def init_all():
    begin = datetime.datetime.now()
    print '开始初始化任务 {0: %Y-%m-%d %H:%M:%S}'.format(begin)
    site_list = session.query(Site).all()
    for site in site_list:
        init_base_info(site.slug)
        init_st = add_timezone_to_naive_time(datetime.datetime(2017, 1, 1))
        init_et = add_timezone_to_naive_time(datetime.datetime.now())
        detla = datetime.timedelta(days=3)
        et = init_st
        while 1:
            st = et
            et = et + detla
            init_day_record(site.slug, st, et)
            if et > init_et:
                break
    end = datetime.datetime.now()
    print '结束初始化任务 {0: %Y-%m-%d %H:%M:%S}'.format(end)
    print '共计耗时 {0} 分钟'.format((end - begin).seconds / 60.0)


if __name__ == '__main__':
    init_all()
