# coding: utf-8
from __future__ import unicode_literals

import json
import os

import datetime
import redis
import logging
import requests

from celery import Celery

from drilling.tanks import get_tank_info, get_tank_temperature, get_tank_value, get_inventory_record

app = Celery('tasks', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')

app.config_from_object('drilling.celery_config')


@app.task()
def get_tanks():
    logging.info('start get tank info')
    get_tank_info('test')
    get_tank_temperature('test')
    get_tank_value('test')
    logging.info('success get tank info')


@app.task()
def get_inventory_record_task():
    logging.info('start get inventory record')
    get_inventory_record('test', datetime.datetime(2017, 5, 1), datetime.datetime(2017, 5, 2))
    logging.info('success get inventory record')
