# coding: utf-8
from __future__ import unicode_literals

import datetime
import pytz

from drilling.models import session, Site, FuelTank


def get_site_by_slug(slug):
    obj = session.query(Site).filter(Site.slug == slug).first()
    return obj if obj else None


def create_tank(tid, site_id, *args, **kwargs):
    obj = FuelTank()
    obj.tank_id = tid,
    obj.name = ''
    obj.belong_id = site_id
    obj.create_time = datetime.datetime.now()
    for k, v in kwargs:
        setattr(obj, k, v)
    session.add(obj)
    session.commit()
    return obj


def get_tank_by_tank_id(tid, site_id, *args, **kwargs):
    obj = session.query(FuelTank).filter(FuelTank.tank_id == tid, FuelTank.belong_id == site_id).first()
    if not obj:
        obj = create_tank(tid, site_id, *args, **kwargs)
    return obj


def add_timezone_to_naive_time(time_obj):
    obj = time_obj.replace(tzinfo=pytz.timezone('Asia/Shanghai'))
    return obj
