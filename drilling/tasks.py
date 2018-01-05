# coding: utf-8
from __future__ import unicode_literals

import json
import os

import datetime
import redis
import logging
import requests

from celery.schedules import crontab
from celery import Celery

from drilling.fuels import get_fuel_order, get_delivery
# from drilling.models import session, Site
from drilling.store import get_store_order, get_inventories
from drilling.tanks import get_tank_info, get_tank_temperature, get_tank_value, get_inventory_record

app = Celery('tasks', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')

app.config_from_object('drilling.celery_config')


@app.on_after_configure.connect
def init_periodic_tasks(sender, **kwargs):
    # site_list = [itm[0] for itm in session.query(Site.slug).all()]
    site_list = ['test']
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
            crontab(hour=7, minute=30, day_of_week=1),
            get_inventories_task.s(site),
        )


@app.task()
def get_tank_info_task(site):
    task_info = 'get tank info {0}'.format(site)
    logging.info('START {0}'.format(task_info))
    get_tank_info(site)
    get_tank_temperature(site)
    get_tank_value(site)
    logging.info('SUCCESS {0}'.format(task_info))


@app.task()
def get_inventory_record_task(site):
    task_info = 'get inventory record {0}'.format(site)
    logging.info('START {0}'.format(task_info))
    get_inventory_record(site)
    logging.info('SUCCESS {0}'.format(task_info))


@app.task()
def get_fuel_order_task(site):
    task_info = 'get fuel order {0}'.format(site)
    logging.info('START {0}'.format(task_info))
    get_fuel_order(site)
    logging.info('SUCCESS {0}'.format(task_info))


@app.task()
def get_delivery_task(site):
    task_info = 'get delivery {0}'.format(site)
    logging.info('START {0}'.format(task_info))
    get_delivery(site)
    logging.info('SUCCESS {0}'.format(task_info))


@app.task()
def get_store_order_task(site):
    task_info = 'get store order {0}'.format(site)
    logging.info('START {0}'.format(task_info))
    get_store_order(site)
    logging.info('SUCCESS {0}'.format(task_info))


@app.task()
def get_inventories_task(site):
    task_info = 'get store order {0}'.format(site)
    logging.info('START {0}'.format(task_info))
    get_inventories(site)
    logging.info('SUCCESS {0}'.format(task_info))




