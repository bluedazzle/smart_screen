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
from drilling.fuels import get_fuel_order, get_delivery
from drilling.init import init_all, init_in_test
from drilling.models import session, Site, CeleryLog
from drilling.store import get_store_order, get_inventories
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
        log.err_info = exc
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
    # site_list = [itm[0] for itm in session.query(Site.slug).all()]
    site_list = ['mf', '54', 'air']
    for site in site_list:
        sender.add_periodic_task(
            datetime.timedelta(seconds=40),
            # crontab(hour=7, minute=30, day_of_week=1),
            get_tank_info_task.s(site),
        )
        sender.add_periodic_task(
            datetime.timedelta(seconds=30),
            get_inventory_record_task.s(site),
        )
        sender.add_periodic_task(
            datetime.timedelta(seconds=25),
            get_fuel_order_task.s(site),
        )
        sender.add_periodic_task(
            datetime.timedelta(seconds=35),
            get_store_order_task.s(site),
        )
        sender.add_periodic_task(
            datetime.timedelta(seconds=45),
            get_delivery_task.s(site),
        )
        sender.add_periodic_task(
            crontab(hour=4, minute=30),
            get_inventories_task.s(site),
        )
        sender.add_periodic_task(
            datetime.timedelta(seconds=20),
            get_card_record_task.s(site),
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
def init_test(self, site):
    task_info = 'init task site {0}'.format(site)
    logging.info('START {0}'.format(task_info))
    init_in_test(site, self.request.get('id'))
    logging.info('SUCCESS {0}'.format(task_info))
