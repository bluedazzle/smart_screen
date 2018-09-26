# coding: utf-8
from __future__ import unicode_literals

import datetime
import hashlib

import logging

import math
import pytz
import redis
from xpinyin import Pinyin

from drilling.models import session, Site, FuelTank, InventoryRecord, FuelOrder, Classification, SecondClassification, \
    ThirdClassification, GoodsOrder, Supplier, Receiver, GoodsInventory, AbnormalRecord, CardRecord

PINYIN = Pinyin()


def get_site_by_slug(slug):
    obj = session.query(Site).filter(Site.slug == slug).first()
    return obj if obj else None


def update_site_status(site, msg):
    cache = redis.StrictRedis(db=2)
    now = get_now_time_with_timezone()
    encode_msg = '{0}|$|{1: %Y-%m-%d %H:%M:%S}'.format(msg, now)
    cache.set('site_{0}'.format(site.slug), encode_msg)


def create_tank(tid, site_id, *args, **kwargs):
    obj = FuelTank()
    obj.tank_id = tid,
    obj.name = ''
    obj.belong_id = site_id
    obj.create_time = get_now_time_with_timezone()
    for k, v in kwargs.items():
        setattr(obj, k, v)
    session.add(obj)
    try:
        session.commit()
    except Exception as e:
        logging.exception('ERROR in commit session site {0} reason {1}'.format(site_id, e))
        session.rollback()
    return obj


def create_record(**kwargs):
    obj = InventoryRecord()
    obj.create_time = get_now_time_with_timezone()
    for k, v in kwargs.items():
        if not v:
            v = 0.0
        if isinstance(v, datetime.datetime):
            v = add_timezone_to_naive_time(v)
        setattr(obj, k, v)
    session.add(obj)
    try:
        session.commit()
    except Exception as e:
        logging.exception('ERROR in commit session site {0} reason {1}'.format(kwargs.get('belong_id'), e))
        session.rollback()
    logging.info('INFO create record {0: %Y-%m-%d %H:%M:%S} success'.format(obj.original_create_time))
    return obj


def create_card_record(**kwargs):
    obj = CardRecord()
    obj.create_time = get_now_time_with_timezone()
    obj.modify_time = get_now_time_with_timezone()
    for k, v in kwargs.items():
        if isinstance(v, datetime.datetime):
            v = add_timezone_to_naive_time(v)
        setattr(obj, k, v)
    session.add(obj)
    try:
        session.commit()
    except Exception as e:
        logging.exception('ERROR in commit session site {0} reason {1}'.format(kwargs.get('belong_id'), e))
        session.rollback()
    logging.info('INFO create card record {0} success'.format(obj.original_create_time))


def check_card_record(unique_id):
    res = session.query(CardRecord).filter(CardRecord.parent_id == unique_id).all()
    return True if res else False


def create_fuel_order(**kwargs):
    obj = FuelOrder()
    obj.create_time = get_now_time_with_timezone()
    for k, v in kwargs.items():
        if isinstance(v, datetime.datetime):
            v = add_timezone_to_naive_time(v)
        setattr(obj, k, v)
    session.add(obj)
    try:
        session.commit()
    except Exception as e:
        logging.exception('ERROR in commit session site {0} reason {1}'.format(kwargs.get('belong_id'), e))
        session.rollback()
    logging.info('INFO create fuel order {0: %Y-%m-%d %H:%M:%S} success'.format(obj.original_create_time))


def create_object(obj_class, **kwargs):
    obj = obj_class()
    obj.create_time = get_now_time_with_timezone()
    for k, v in kwargs.items():
        if isinstance(v, datetime.datetime):
            v = add_timezone_to_naive_time(v)
        setattr(obj, k, v)
    session.add(obj)
    try:
        session.commit()
    except Exception as e:
        logging.exception('ERROR in commit session site {0} reason {1}'.format(kwargs.get('belong_id'), e))
        session.rollback()
    logging.info('INFO create obj {0: %Y-%m-%d %H:%M:%S} success'.format(obj.original_create_time))


def create_goods_order(**kwargs):
    obj = GoodsOrder()
    obj.create_time = get_now_time_with_timezone()
    for k, v in kwargs.items():
        if isinstance(v, datetime.datetime):
            v = add_timezone_to_naive_time(v)
        setattr(obj, k, v)
    session.add(obj)
    try:
        session.commit()
    except Exception as e:
        logging.exception('ERROR in commit session site {0} reason {1}'.format(kwargs.get('belong_id'), e))
        session.rollback()
    logging.info('INFO create goods order {0: %Y-%m-%d %H:%M:%S} success'.format(obj.original_create_time))


def get_latest_settlement_record(tank_id):
    obj = session.query(InventoryRecord).filter(InventoryRecord.record_type == 3,
                                                InventoryRecord.tank_id == tank_id).order_by(
        InventoryRecord.original_create_time.desc()).first()
    return obj


def get_record_by_hash(hash_str):
    obj = session.query(InventoryRecord).filter(InventoryRecord.hash == hash_str).first()
    return obj


def get_obj_by_hash(hash_str, obj_class):
    try:
        obj = session.query(obj_class).filter(obj_class.hash == hash_str).first()
        return obj
    except Exception as e:
        print e
        return None


def get_goods_order_by_hash(hash_str):
    try:
        obj = session.query(GoodsOrder).filter(GoodsOrder.hash == hash_str).first()
        return obj
    except Exception as e:
        print e
        return None


def get_fuel_order_by_hash(hash_str):
    try:
        obj = session.query(FuelOrder).filter(FuelOrder.hash == hash_str).first()
        return obj
    except Exception as e:
        print e
        return None


def get_tank_by_tank_id(tid, site_id, *args, **kwargs):
    obj = session.query(FuelTank).filter(FuelTank.tank_id == tid, FuelTank.belong_id == site_id).first()
    if not obj:
        obj = create_tank(tid, site_id, *args, **kwargs)
    return obj


def get_object_by_id(oid, site, obj_class):
    obj = session.query(obj_class).filter(obj_class.id == oid, obj_class.belong_id == site.id).first()
    return obj


def get_sup_by_sid(sid, site):
    obj = session.query(Supplier).filter(Supplier.sid == sid, Supplier.belong_id == site.id).first()
    return obj


def get_rev_by_rid(rid, site):
    obj = session.query(Receiver).filter(Receiver.rid == rid, Receiver.belong_id == site.id).first()
    return obj


def get_all_tanks_by_site(site):
    objs = session.query(FuelTank).filter(FuelTank.belong_id == site.id).all()
    return objs


def get_goods_inventory_by_barcode(barcode, site):
    obj = session.query(GoodsInventory).filter(GoodsInventory.barcode == barcode,
                                               GoodsInventory.belong_id == site.id).first()
    return obj


def add_timezone_to_naive_time(time_obj):
    if not time_obj:
        logging.warning('WARNING in add tzinfo to time, reason: time_obj is None ')
        return get_now_time_with_timezone()
    if time_obj.tzinfo:
        return time_obj
    tz = pytz.timezone('Asia/Shanghai')
    aware_time = tz.localize(time_obj)
    # obj = time_obj.replace(tzinfo=pytz.timezone('Asia/Shanghai'))
    return aware_time


def generate_hash(*args):
    string = ''.join(args)
    return hashlib.md5(string).hexdigest()


def get_clean_data(value):
    try:
        return value.strip().decode('gbk')
    except Exception as e:
        logging.exception('ERROR IN get clean data reason {0}'.format(e))
        return '错误'


def datetime_to_string(obj, fmt='%Y-%m-%d'):
    return obj.strftime(fmt)


def get_second_cls_by_id(cid):
    res = session.query(SecondClassification).filter(SecondClassification.id == cid).first()
    return res


def get_now_time_with_timezone():
    now = datetime.datetime.now()
    now = add_timezone_to_naive_time(now)
    return now


def update_sup(sid, site, **kwargs):
    res = session.query(Supplier).filter(Supplier.sid == sid, Supplier.belong_id == site.id).first()
    if not res:
        res = Supplier()
        res.sid = sid
        res.belong_id = site.id
    for k, v in kwargs.items():
        setattr(res, k, v)
    session.add(res)
    try:
        session.commit()
    except Exception as e:
        logging.exception('ERROR in commit session site {0} reason {1}'.format(kwargs.get('belong_id'), e))
        session.rollback()
    return res


def update_rev(rid, site, **kwargs):
    res = session.query(Receiver).filter(Receiver.rid == rid, Receiver.belong_id == site.id).first()
    if not res:
        res = Receiver()
        res.rid = rid
        res.belong_id = site.id
    for k, v in kwargs.items():
        setattr(res, k, v)
    session.add(res)
    try:
        session.commit()
    except Exception as e:
        logging.exception('ERROR in commit session site {0} reason {1}'.format(kwargs.get('belong_id'), e))
        session.rollback()
    return res


def update_classification(cid, **kwargs):
    res = session.query(Classification).filter(Classification.id == cid).first()
    if not res:
        res = Classification()
        res.create_time = get_now_time_with_timezone()
        res.id = cid
    for k, v in kwargs.items():
        setattr(res, k, v)
    res.original_create_time = get_now_time_with_timezone()
    session.add(res)
    try:
        session.commit()
    except Exception as e:
        logging.exception('ERROR in commit session site {0} reason {1}'.format(kwargs.get('belong_id'), e))
        session.rollback()
    return res


def update_second_classification(cid, **kwargs):
    res = session.query(SecondClassification).filter(SecondClassification.id == cid).first()
    if not res:
        res = SecondClassification()
        res.create_time = get_now_time_with_timezone()
        res.id = cid
    for k, v in kwargs.items():
        setattr(res, k, v)
    res.original_create_time = get_now_time_with_timezone()
    session.add(res)
    try:
        session.commit()
    except Exception as e:
        logging.exception('ERROR in commit session site {0} reason {1}'.format(kwargs.get('belong_id'), e))
        session.rollback()
    return res


def update_third_classification(cid, **kwargs):
    res = session.query(ThirdClassification).filter(ThirdClassification.id == cid).first()
    if not res:
        res = ThirdClassification()
        res.create_time = get_now_time_with_timezone()
        res.id = cid
    for k, v in kwargs.items():
        setattr(res, k, v)
    res.original_create_time = get_now_time_with_timezone()
    second_cls = get_second_cls_by_id(kwargs.get('parent_id'))
    if second_cls:
        res.grandparent_id = second_cls.parent_id
    session.add(res)
    try:
        session.commit()
    except Exception as e:
        logging.exception('ERROR in commit session site {0} reason {1}'.format(kwargs.get('belong_id'), e))
        session.rollback()
    return res


def update_goods_inventory(hash_str, **kwargs):
    gi = get_obj_by_hash(hash_str, GoodsInventory)
    if not gi:
        gi = GoodsInventory()
        gi.create_time = get_now_time_with_timezone()
        gi.original_create_time = get_now_time_with_timezone()
        gi.last_sell_time = add_timezone_to_naive_time(datetime.datetime(2017, 1, 1))
    for k, v in kwargs.items():
        setattr(gi, k, v)
    gi.modify_time = get_now_time_with_timezone()
    session.add(gi)
    try:
        session.commit()
    except Exception as e:
        logging.exception('ERROR in commit session site {0} reason {1}'.format(kwargs.get('belong_id'), e))
        session.rollback()
    return gi


def query_by_pagination(site, session, obj, total, order_by='id', start_offset=0, limit=1000):
    total_page = int(math.ceil(total / float(limit)))
    start = 0
    if start_offset:
        start = start_offset / limit

    for i in xrange(start, total_page):
        offset = limit * i
        result = session.query(obj).filter(obj.catch_payment == False).order_by(order_by).limit(limit).offset(
            offset).all()
        logging.info(
            '{0}: Current {1}->{2}/{3} {4}%'.format(site.slug, offset, offset + limit, total, float(offset + limit) / total * 100))
        yield result


def create_abnormal_record(abnormal_type, **kwargs):
    if abnormal_type == 1:
        st, et = get_today_st_et()
    else:
        st, et = get_week_st_et()
    obj = AbnormalRecord()
    obj.create_time = get_now_time_with_timezone()
    obj.start_time = st
    obj.end_time = et
    obj.abnormal_type = abnormal_type
    for k, v in kwargs.items():
        setattr(obj, k, v)
    session.add(obj)
    try:
        session.commit()
    except Exception as e:
        logging.exception('ERROR in commit session site {0} reason {1}'.format(kwargs.get('belong_id'), e))
        session.rollback()
    logging.info('INFO create abnormal record {0: %Y-%m-%d %H:%M:%S} success'.format(obj.create_time))
    return obj


def string_to_datetime(time_data, fmt='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.strptime(time_data, fmt)


def get_today_st_et():
    now = datetime.datetime.now()
    st = add_timezone_to_naive_time(datetime.datetime(now.year, now.month, now.day))
    et = add_timezone_to_naive_time(datetime.datetime(now.year, now.month, now.day, 23, 59, 59))
    return st, et


def get_today_night():
    now = datetime.datetime.now()
    st = add_timezone_to_naive_time(datetime.datetime(now.year, now.month, now.day, 6, 0, 0))
    et = add_timezone_to_naive_time(datetime.datetime(now.year, now.month, now.day, 22, 0, 0))
    return st, et


def get_week_st_et():
    now = datetime.datetime.now()
    now_0 = datetime.datetime(now.year, now.month, now.day)
    st = add_timezone_to_naive_time(now_0 - datetime.timedelta(days=now.weekday()))
    et = add_timezone_to_naive_time(now_0 + datetime.timedelta(days=6 - now.weekday()))
    return st, et


def get_py(name):
    try:
        res = PINYIN.get_initials(name, '').replace(' ', '')
        return res
    except Exception as e:
        logging.exception('ERROR in get pinyin {0} reason {1}'.format(name, e))
        return ''


if __name__ == '__main__':
    print string_to_datetime('2017-01-01 00:00:00')
