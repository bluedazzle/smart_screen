# coding: utf-8
from __future__ import unicode_literals

import datetime
import logging

import redis

from drilling.card import get_card_record
from drilling.const import TaskStatus
from drilling.fuels import get_sup, get_rev, get_delivery, get_fuel_order
from drilling.models import session, Site, Task
from drilling.store import get_first_classify, get_second_classify, get_third_classify, get_inventories, get_store_order
from drilling.tanks import get_tank_info, get_tank_value, get_tank_temperature, get_tank_grade, get_inventory_record
from drilling.utils import add_timezone_to_naive_time, get_now_time_with_timezone


def update_init_progress(task, percent, msg, status=TaskStatus.running):
    logging.info(msg)
    if not task:
        return
    cache = redis.StrictRedis(db=2)
    encode_msg = '{0}|$|{1}|$|{2}'.format(status, percent, msg)
    cache.set(task, encode_msg)


def init_base_info(site, task_id):
    get_tank_info(site)
    get_tank_value(site)
    get_tank_temperature(site)
    get_tank_grade(site)
    logging.info('{0}:成功获取油罐信息'.format(site))

    get_sup(site)
    get_rev(site)
    logging.info('{0}: 成功获取运送基本信息'.format(site))

    get_first_classify(site)
    get_second_classify(site)
    get_third_classify(site)
    logging.info('{0}: 成功获取分类基本信息'.format(site))

    get_inventories(site)
    logging.info('{0}: 成功获取库存基本信息'.format(site))
    update_init_progress(task_id, 1, '成功获取基本信息')


def init_day_record(site, st, et, task_id, percent):
    get_inventory_record(site, st, et)
    msg = '{0}: 成功获取{1: %Y-%m-%d}~{2: %Y-%m-%d}油库记录'.format(site, st, et)
    update_init_progress(task_id, percent, msg)
    get_delivery(site, st, et)
    msg = '{0}: 成功获取{1: %Y-%m-%d}~{2: %Y-%m-%d}送货记录'.format(site, st, et)
    update_init_progress(task_id, percent, msg)
    get_fuel_order(site, st, et)
    msg = '{0}: 成功获取{1: %Y-%m-%d}~{2: %Y-%m-%d}油品订单'.format(site, st, et)
    update_init_progress(task_id, percent, msg)
    get_store_order(site, st, et)
    msg = '{0}: 成功获取{1: %Y-%m-%d}~{2: %Y-%m-%d}非油订单'.format(site, st, et)
    update_init_progress(task_id, percent, msg)
    get_card_record(site, st, et)
    msg = '{0}: 成功获取{1: %Y-%m-%d}~{2: %Y-%m-%d}卡数据'.format(site, st, et)
    update_init_progress(task_id, percent, msg)


def init_all(slug, task_id=None):
    try:
        begin = datetime.datetime.now()
        now = get_now_time_with_timezone()
        logging.info('开始初始化任务 {0: %Y-%m-%d %H:%M:%S}'.format(begin))
        site = session.query(Site).filter(Site.slug == slug).first()
        if site:
            task = Task()
            task.task_id = task_id
            task.belong_id = site.id
            task.name = '初始化任务: {0}'.format(site.name)
            task.create_time = now
            task.original_create_time = now
            task.modify_time = now
            session.add(task)
            try:
                session.commit()
            except Exception as e:
                logging.exception('ERROR in commit session site {0} reason {1}'.format(slug, e))
                session.rollback()

            init_base_info(site.slug, task_id)
            init_st = add_timezone_to_naive_time(datetime.datetime(2016, 12, 15))
            init_et = add_timezone_to_naive_time(datetime.datetime.now())
            total_days = (init_et - init_st).days
            times = total_days / 7
            detla = datetime.timedelta(days=7)
            count = 0.0
            et = init_st
            while 1:
                st = et
                et = et + detla
                count += 1
                percent = round(count / times, 2) * 100
                init_day_record(site.slug, st, et, task_id, percent)
                if st > init_et:
                    break
        end = datetime.datetime.now()
        msg = '结束初始化任务 {0: %Y-%m-%d %H:%M:%S} 共计耗时 {1} 分钟'.format(end, round((end - begin).seconds / 60.0))
        update_init_progress(task_id, 100, msg, TaskStatus.finish)
    except Exception as e:
        logging.exception('ERROR in init all site {0} reason {1}'.format(slug, e))
        update_init_progress(task_id, 0, e.message, TaskStatus.error)
        raise e


def get_missing(slug, task_id=None):
    try:
        begin = datetime.datetime.now()
        now = get_now_time_with_timezone()
        logging.info('开始初始化任务 {0: %Y-%m-%d %H:%M:%S}'.format(begin))
        site = session.query(Site).filter(Site.slug == slug).first()
        if site:
            task = Task()
            task.task_id = task_id
            task.belong_id = site.id
            task.name = '初始化任务: {0}'.format(site.name)
            task.create_time = now
            task.original_create_time = now
            task.modify_time = now
            session.add(task)
            try:
                session.commit()
            except Exception as e:
                logging.exception('ERROR in commit session site {0} reason {1}'.format(slug, e))
                session.rollback()

            init_st = add_timezone_to_naive_time(datetime.datetime(2017, 5, 1))
            init_et = add_timezone_to_naive_time(datetime.datetime.now())
            total_days = (init_et - init_st).days
            times = total_days / 7
            detla = datetime.timedelta(days=7)
            count = 0.0
            et = init_st
            while 1:
                st = et
                et = et + detla
                count += 1
                percent = round(count / times, 2) * 100
                init_day_record(site.slug, st, et, task_id, percent)
                if st > init_et:
                    break
        end = datetime.datetime.now()
        msg = '结束初始化任务 {0: %Y-%m-%d %H:%M:%S} 共计耗时 {1} 分钟'.format(end, round((end - begin).seconds / 60.0))
        update_init_progress(task_id, 100, msg, TaskStatus.finish)
    except Exception as e:
        logging.exception('ERROR in init all site {0} reason {1}'.format(slug, e))
        update_init_progress(task_id, 0, e.message, TaskStatus.error)
        raise e


def init_in_test(slug, task_id=None):
    import time
    try:
        begin = datetime.datetime.now()
        now = get_now_time_with_timezone()
        logging.info('开始初始化任务 {0: %Y-%m-%d %H:%M:%S}'.format(begin))
        site = session.query(Site).filter(Site.slug == slug).first()
        if site:
            task = Task()
            task.task_id = task_id
            task.belong_id = site.id
            task.name = '初始化任务: {0}'.format(site.name)
            task.create_time = now
            task.original_create_time = now
            task.modify_time = now
            session.add(task)
            try:
                session.commit()
            except Exception as e:
                logging.exception('ERROR in commit session site {0} reason {1}'.format(slug, e))
                session.rollback()

            init_st = add_timezone_to_naive_time(datetime.datetime(2016, 12, 15))
            init_et = add_timezone_to_naive_time(datetime.datetime.now())
            total_days = (init_et - init_st).days
            times = total_days / 7
            detla = datetime.timedelta(days=7)
            count = 0.0
            et = init_st
            while 1:
                st = et
                et = et + detla
                count += 1
                percent = round(count / times, 2) * 100
                update_init_progress(task_id, percent, '任务执行中')
                time.sleep(0.5)
                if st > init_et:
                    break
        end = datetime.datetime.now()
        msg = '结束初始化任务 {0: %Y-%m-%d %H:%M:%S} 共计耗时 {1} 分钟'.format(end, (end - begin).seconds / 60.0)
        update_init_progress(task_id, 100, msg, TaskStatus.finish)
    except Exception as e:
        logging.exception('ERROR in init all site {0} reason {1}'.format(slug, e))
        session.rollback()
        update_init_progress(task_id, 0, e.message, TaskStatus.error)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    init_all('air')

