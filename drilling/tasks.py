# coding: utf-8
from __future__ import unicode_literals

import json
import os
import redis
import logging
import requests

from celery import Celery

from smart_screen.drilling.fb import get_tank

app = Celery('tasks', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')

app.config_from_object('smart_screen.drilling.celery_config')


@app.task()
def test_tank():
    logging.info('start get tank tmp')
    # get_tank()
    print 'catch'
    logging.info('success get tank tmp')
