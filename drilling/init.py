# coding: utf-8
from __future__ import unicode_literals

import datetime
import logging

from drilling.card import get_card_record
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
    logging.info('{0}:成功获取油罐信息'.format(site).encode('utf-8'))

    get_sup(site)
    get_rev(site)
    logging.info('{0}: 成功获取运送基本信息'.format(site).encode('utf-8'))

    get_first_classify(site)
    get_second_classify(site)
    get_third_classify(site)
    logging.info('{0}: 成功获取分类基本信息'.format(site).encode('utf-8'))

    get_inventories(site)
    logging.info('{0}: 成功获取库存基本信息'.format(site).encode('utf-8'))


def init_day_record(site, st, et):
    get_inventory_record(site, st, et)
    logging.info('{0}: 成功获取{1: %Y-%m-%d}~{2: %Y-%m-%d}油库记录'.format(site, st, et).encode('utf-8'))
    get_delivery(site, st, et)
    logging.info('{0}: 成功获取{1: %Y-%m-%d}~{2: %Y-%m-%d}送货记录'.format(site, st, et).encode('utf-8'))
    get_fuel_order(site, st, et)
    logging.info('{0}: 成功获取{1: %Y-%m-%d}~{2: %Y-%m-%d}油品订单'.format(site, st, et).encode('utf-8'))
    get_store_order(site, st, et)
    logging.info('{0}: 成功获取{1: %Y-%m-%d}~{2: %Y-%m-%d}非油订单'.format(site, st, et).encode('utf-8'))
    get_card_record(site, st, et)
    logging.info('{0}: 成功获取{1: %Y-%m-%d}~{2: %Y-%m-%d}卡数据'.format(site, st, et).encode('utf-8'))


def init_all():
    begin = datetime.datetime.now()
    logging.info('开始初始化任务 {0: %Y-%m-%d %H:%M:%S}'.format(begin).encode('utf-8'))
    site_list = session.query(Site).filter(Site.slug == 'air').all()
    for site in site_list:
        # init_base_info(site.slug)
        init_st = add_timezone_to_naive_time(datetime.datetime(2017, 1, 1))
        init_et = add_timezone_to_naive_time(datetime.datetime.now())
        detla = datetime.timedelta(days=7)
        et = init_st
        while 1:
            st = et
            et = et + detla
            init_day_record(site.slug, st, et)
            if st > init_et:
                break
    end = datetime.datetime.now()
    logging.info('结束初始化任务 {0: %Y-%m-%d %H:%M:%S}'.format(end).encode('utf-8'))
    logging.info('共计耗时 {0} 分钟'.format((end - begin).seconds / 60.0).encode('utf-8'))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    init_all()
