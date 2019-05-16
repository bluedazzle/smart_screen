# coding: utf-8
from __future__ import unicode_literals

import json
import os

import datetime
import redis
import logging
import requests
from celery import Task

from celery.schedules import crontab
from celery import Celery

from drilling.card import get_card_record
from drilling.db.session import with_session
from drilling.fuels import get_fuel_order, get_delivery, get_fuel_order_payment
from drilling.init import init_all, init_in_test, get_missing
from drilling.models import session, Site, CeleryLog
from drilling.store import get_store_order, get_inventories, get_goods_order_payment
from drilling.tanks import get_tank_info, get_tank_temperature, get_tank_value, get_inventory_record, get_tank_grade
from drilling.utils import get_now_time_with_timezone, get_site_by_slug

app = Celery('tasks', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')

app.config_from_object('drilling.celery_config')


class OilTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        now = get_now_time_with_timezone()
        site = get_site_by_slug(args[0])
        logging.info('task done: {0}'.format(retval))
        log = CeleryLog()
        log.task_id = task_id
        log.task_type = 1
        log.status = 1
        log.err_info = ''
        log.create_time = now
        log.modify_time = now
        log.belong_id = site.id
        log.original_create_time = now
        session.add(log)
        try:
            session.commit()
        except Exception as e:
            logging.exception('ERROR in commit session task {0} reason {1}'.format(task_id, e))
            session.rollback()
        return super(OilTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        now = get_now_time_with_timezone()
        site = get_site_by_slug(args[0])
        logging.exception('task fail, reason: {0}'.format(exc))
        log = CeleryLog()
        log.task_id = task_id
        log.task_type = 1
        log.status = 0
        log.create_time = now
        log.modify_time = now
        log.original_create_time = now
        log.err_info = einfo
        log.belong_id = site.id
        session.add(log)
        try:
            session.commit()
        except Exception as e:
            logging.exception('ERROR in commit session task {0} reason {1}'.format(task_id, e))
            session.rollback()
        return super(OilTask, self).on_failure(exc, task_id, args, kwargs, einfo)


@app.on_after_configure.connect
def init_periodic_tasks(sender, **kwargs):
    #site_list = [itm[0] for itm in session.query(Site.slug).filter(Site.check == True).all()]
    #site_list = site_list[0:10]
    # site_list = [u'mf', u'54']
    # site_list = [u'NJJYZ', u'TALJYZ', u'DLJYZ48', u'JZXCJYZ', u'DLSLJYZ', u'DCDXCKJYZ', u'NDJYZ', u'CNJYZ', u'LDBHZ', u'DLHJYZ', u'YJZJYZ', u'QLLJYZ', u'GHTJYZ', u'SLQJYZ', u'DG', u'DH', u'GHFWQNZ', u'DCDJYZ', u'DJZZ', u'CKYHZ', u'GDHDZ', u'XDJYZ', u'BJJYZ', u'GNCXZ', u'HNXCJYZ', u'SCKJYZ', u'QLCDZ', u'HLALGSTCQ', u'HBXHZ', u'DLHKLJYZ', u'PAZXZ', u'PAPMZ', u'XHXCZ', u'MQJYZ', u'DRJYZ', u'BMJYZ', u'XZJYZ', u'GHJYL', u'JGJYZ', u'SMCJYZ', u'NQJYZ', u'HXGEMDZ', u'XHJYZ', u'BYLJYZ', u'XKJYZ', u'mf', u'BSHJYZ', u'DXJYZ', u'SXZGYYQJYZ', u'XHJZZ', u'HZWYZ', u'BHJYZ32', u'YQZLJYZ', u'air', u'QTJYZ', u'DMJYZ', u'DCDGDXCKJYZ', u'JSMJYZ', u'LDHHZ', u'MHSNZ', u'XMJYZ', u'MHMLWZ', u'DLJYZ', u'BCJYZ', u'SQJYZ', u'HHQJYZ', u'SMJYZ', u'KFQJYZ', u'YJKJYZ', u'BHJYZ', u'DEJYZ', u'RYZ', u'CHSZ', u'GHFWQBZ', u'DTHZ', u'GDGLZ', u'GCCDZ', u'HBCXZ', u'PAYFZ', u'MHXCZ', u'HLQKDZ', u'TJEZ', u'WLJT(DE)JYZ', u'XHDDJZ', u'PAPXZ', u'GZJYZ', u'CDMLJYZ', u'TSJYZ', u'TDXZ', u'TRNDHCRKJYZ', u'ZKXCJYZ', u'DWJYZ', u'54', u'TJTMZ', u'151Z', u'HYZ', u'XJYJYZ', u'HNDEJYZ', u'QJJYZ', u'NSKJYZ', u'HZDHZ', u'SWYQJYZ', u'YKGLJYZ', u'DCDJYZ1', u'SBJYZ', u'DLHCJLJYZ', u'TJSZ', u'DLHQXJYZ', u'JZJYZ', u'QSHJYZ', u'CJNLJYZ', u'HHLJYZ']
    site_list = ['QSHJYZ',u'XMJYZ',u'SMCJYZ',u'BJJYZ',u'JZXCJYZ',u'151Z',u'LDHHZ',u'HHQJYZ',u'BMJYZ',u'XZJYZ',u'GHJYL',u'ZKXCJYZ',u'HNXCJYZ',u'TSJYZ',u'PAZXZ',u'JGJYZ',u'air',u'DMJYZ',u'SLQJYZ',u'SQJYZ',u'NQJYZ',u'BHJYZ',u'NJJYZ',u'KFQJYZ',u'XJYJYZ',u'CNJYZ',u'QLLJYZ',u'PAYFZ',u'JZJYZ',u'DRJYZ',u'CDMLJYZ',u'CJNLJYZ',u'DCDJYZ',u'WLJT(DE)JYZ',u'SCKJYZ',u'YJZJYZ',u'TJSZ',u'YJKJYZ',u'BCJYZ',u'DWJYZ',u'DLHJYZ',u'GHTJYZ',u'FTJYZ',u'SWYQJYZ',u'QTJYZ',u'HHLJYZ',u'XDJYZ',u'SXZGYYQJYZ',u'mf',u'ZZJYZ',u'HYZ',u'SMJYZ',u'HNDEJYZ',u'YQZLJYZ',u'DJZZ',u'HBXHZ',u'BHJYZ32',u'PAPMZ',u'DLJYZ',u'XHJYZ',u'54',u'MQJYZ',u'DLJYZ48',u'HBCXZ']
    for site in site_list:
        logging.info('start site: {}'.format(site))
	sender.add_periodic_task(
            datetime.timedelta(seconds=50),
            # crontab(hour=7, minute=30, day_of_week=1),
            get_tank_info_task.s(site),
        )
        sender.add_periodic_task(
            datetime.timedelta(minutes=5),
            get_inventory_record_task.s(site),
        )
        sender.add_periodic_task(
            datetime.timedelta(seconds=80),
            get_fuel_order_task.s(site),
        )
        sender.add_periodic_task(
            datetime.timedelta(minutes=1),
            get_store_order_task.s(site),
        )
        sender.add_periodic_task(
            datetime.timedelta(minutes=5),
            get_delivery_task.s(site),
        )
        sender.add_periodic_task(
            crontab(hour=4, minute=30),
            get_inventories_task.s(site),
        )
        sender.add_periodic_task(
            datetime.timedelta(seconds=50),
            get_card_record_task.s(site),
        )
        sender.add_periodic_task(
            datetime.timedelta(minutes=480),
            get_fuel_payments.s(site),
        )
        sender.add_periodic_task(
            datetime.timedelta(minutes=470),
            get_goods_payments.s(site),
        )


@app.task()
@with_session
def get_tank_info_task(site):
    task_info = 'get tank info {0}'.format(site)
    logging.info('START {0}'.format(task_info))
    get_tank_info(site)
    get_tank_temperature(site)
    get_tank_value(site)
    get_tank_grade(site)
    logging.info('SUCCESS {0}'.format(task_info))


@app.task()
@with_session
def get_inventory_record_task(site):
    task_info = 'get inventory record {0}'.format(site)
    logging.info('START {0}'.format(task_info))
    get_inventory_record(site)
    logging.info('SUCCESS {0}'.format(task_info))


@app.task()
@with_session
def get_fuel_order_task(site):
    task_info = 'get fuel order {0}'.format(site)
    logging.info('START {0}'.format(task_info))
    get_fuel_order(site)
    logging.info('SUCCESS {0}'.format(task_info))


@app.task()
@with_session
def get_delivery_task(site):
    task_info = 'get delivery {0}'.format(site)
    logging.info('START {0}'.format(task_info))
    get_delivery(site)
    logging.info('SUCCESS {0}'.format(task_info))


@app.task()
@with_session
def get_store_order_task(site):
    task_info = 'get store order {0}'.format(site)
    logging.info('START {0}'.format(task_info))
    get_store_order(site)
    logging.info('SUCCESS {0}'.format(task_info))


@app.task()
@with_session
def get_inventories_task(site):
    task_info = 'get store order {0}'.format(site)
    logging.info('START {0}'.format(task_info))
    get_inventories(site)
    logging.info('SUCCESS {0}'.format(task_info))


@app.task()
@with_session
def get_fuel_payments(site, threads=4):
    task_info = 'get fuel order payments {0}'.format(site)
    logging.info('START {0}'.format(task_info))
    site = get_site_by_slug(site)
    get_fuel_order_payment(site, threads, True)
    logging.info('SUCCESS {0}'.format(task_info))


@app.task()
@with_session
def get_goods_payments(site, threads=4):
    task_info = 'get goods order payments {0}'.format(site)
    logging.info('START {0}'.format(task_info))
    site = get_site_by_slug(site)
    get_goods_order_payment(site, threads, True)
    logging.info('SUCCESS {0}'.format(task_info))


@app.task()
@with_session
def get_card_record_task(site):
    task_info = 'get card record {0}'.format(site)
    logging.info('START {0}'.format(task_info))
    get_card_record(site)
    logging.info('SUCCESS {0}'.format(task_info))


@app.task(base=OilTask, bind=True)
@with_session
def init_task(self, site):
    task_info = 'init task site {0}'.format(site)
    logging.info('START {0}'.format(task_info))
    init_all(site, self.request.get('id'))
    logging.info('SUCCESS {0}'.format(task_info))


@app.task(base=OilTask, bind=True)
@with_session
def get_missing_task(self, site):
    task_info = 're-check task site {0}'.format(site)
    logging.info('START {0}'.format(task_info))
    get_missing(site, self.request.get('id'))
    logging.info('SUCCESS {0}'.format(task_info))


@app.task(base=OilTask, bind=True)
@with_session
def init_test(self, site):
    task_info = 'init task site {0}'.format(site)
    logging.info('START {0}'.format(task_info))
    init_in_test(site, self.request.get('id'))
    logging.info('SUCCESS {0}'.format(task_info))

