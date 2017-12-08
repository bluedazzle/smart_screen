# coding: utf-8
from __future__ import unicode_literals

import datetime
import hashlib

import logging
import pytz

from drilling.models import session, Site, FuelTank, InventoryRecord, FuelOrder


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


def create_record(**kwargs):
    obj = InventoryRecord()
    obj.create_time = datetime.datetime.now()
    for k, v in kwargs.items():
        if not v:
            v = 0.0
        if isinstance(v, datetime.datetime):
            v = add_timezone_to_naive_time(v)
        setattr(obj, k, v)
    session.add(obj)
    session.commit()
    logging.info('INFO create record {0: %Y-%m-%d %H:%M:%S} success'.format(obj.original_create_time))
    return obj


def create_fuel_order(**kwargs):
    obj = FuelOrder()
    obj.create_time = datetime.datetime.now()
    for k, v in kwargs.items():
        if isinstance(v, datetime.datetime):
            v = add_timezone_to_naive_time(v)
        setattr(obj, k, v)
    session.add(obj)
    session.commit()
    logging.info('INFO create fuel order {0: %Y-%m-%d %H:%M:%S} success'.format(obj.original_create_time))


def get_latest_settlement_record(tank_id):
    obj = session.query(InventoryRecord).filter(InventoryRecord.record_type == 3,
                                                InventoryRecord.tank_id == tank_id).order_by(
        InventoryRecord.original_create_time.desc()).first()
    return obj


def get_record_by_hash(hash_str):
    obj = session.query(InventoryRecord).filter(InventoryRecord.hash == hash_str).first()
    return obj


def get_fuel_order_by_hash(hash_str):
    obj = session.query(FuelOrder).filter(FuelOrder.hash == hash_str).first()
    return obj


def get_tank_by_tank_id(tid, site_id, *args, **kwargs):
    obj = session.query(FuelTank).filter(FuelTank.tank_id == tid, FuelTank.belong_id == site_id).first()
    if not obj:
        obj = create_tank(tid, site_id, *args, **kwargs)
    return obj


def get_all_tanks_by_site(site):
    objs = session.query(FuelTank).filter(FuelTank.belong_id == site.id).all()
    return objs


def add_timezone_to_naive_time(time_obj):
    tz = pytz.timezone('Asia/Shanghai')
    aware_time = tz.localize(time_obj)
    # obj = time_obj.replace(tzinfo=pytz.timezone('Asia/Shanghai'))
    return aware_time


def generate_hash(*args):
    string = ''.join(args)
    return hashlib.md5(string).hexdigest()


def get_clean_data(value):
    return value.strip().decode('gbk')


def datetime_to_string(obj, fmt='%Y-%m-%d'):
    return obj.strftime(fmt)


def string_to_datetime(time_data, fmt='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.strptime(time_data, format=fmt)
