# coding: utf-8
from __future__ import unicode_literals

import datetime
import redis
import logging
import threading

from drilling.db.interbase import init_interbase_connect
from drilling.models import session, FuelOrder, DeliveryRecord, Receiver, Supplier
from drilling.utils import get_site_by_slug, get_clean_data, get_fuel_order_by_hash, generate_hash, datetime_to_string, \
    create_fuel_order, update_sup, update_rev, get_obj_by_hash, create_object, get_object_by_id, get_rev_by_rid, \
    get_sup_by_sid, query_by_pagination, update_site_status


def get_fuel_order(site, start_time=None, end_time=None):
    if not start_time:
        start_time = datetime.datetime.now() - datetime.timedelta(hours=3)
        end_time = start_time + datetime.timedelta(days=1)
    st = datetime_to_string(start_time)
    et = datetime_to_string(end_time)
    site = get_site_by_slug(site)
    ib_session = init_interbase_connect(site.fuel_server)
    sql = '''select tillnum,timeopen,FULLDESCRIPTION,price,weight,total, tillitem.PUMP_ID, ITEM.DEPT, ITEM.BARCODE from till left
outer join tillitem on (till.tillnum=tillitem.tillnum) and
(till.pos_batch_id=tillitem.pos_batch_id),item,fuel_pumps_hose where tillitem.grade
=item.grade and tillitem.pump_id=fuel_pumps_hose.pump_id and
tillitem.hose_id=fuel_pumps_hose.hose_id and tillitem.STATUSTYPE =1 and timeopen between
'{0}' AND '{1}' and grade>0 order by
virtual_hose_id,timeopen DESC'''.format(st, et)
    ib_session.execute(sql)
    orders = ib_session.fetchall()
    nums = 0
    for order in orders:
        till_id, original_create_time, fuel_type, price, amount, total_price, pump_id, dept, barcode = order
        fuel_type = get_clean_data(fuel_type)
        barcode = get_clean_data(barcode)
        super_dept = unicode(dept)[:6]
        unique_str = generate_hash(unicode(till_id), datetime_to_string(original_create_time, '%Y-%m-%d %H:%M:%S'),
                                   unicode(price), unicode(amount), unicode(pump_id),
                                   unicode(total_price))
        res = get_fuel_order_by_hash(unique_str)
        if res:
            continue
        create_fuel_order(till_id=till_id, original_create_time=original_create_time, fuel_type=fuel_type, price=price,
                          total_price=total_price, amount=amount, pump_id=pump_id, hash=unique_str, belong_id=site.id,
                          classification_id=dept, barcode=barcode, super_cls_id=int(super_dept))
        nums += 1
    logging.info('=============create fuel order {0} site {1}=============='.format(nums, site.name))
    # get_fuel_order_payment(site)
    update_site_status(site, '油品订单更新')


# def get_fuel_order_payment(site):
#     orders = session.query(FuelOrder).filter(FuelOrder.catch_payment == False).all()
#     ib_session = init_interbase_connect(site.fuel_server)
#     for order in orders:
#         sql = '''select TILLITEM_PMNT_SPLIT.PMSUBCODE, PMNT.PMNT_NAME from TILLITEM_PMNT_SPLIT,
# PMNT where TILLITEM_PMNT_SPLIT.TILLNUM={0} AND
# PMNT.PMSUBCODE_ID=TILLITEM_PMNT_SPLIT.PMSUBCODE'''.format(order.till_id)
#         ib_session.execute(sql)
#         res = ib_session.fetchone()
#         if res:
#             payment_code, payment_type = res
#             order.payment_code = payment_code
#             order.payment_type = get_clean_data(payment_type)
#             order.catch_payment = True
#             session.commit()


def get_fuel_order_payment(site, threads=2, today=False):
    t_orders = session.query(FuelOrder.till_id, FuelOrder.id).filter(FuelOrder.catch_payment == False, FuelOrder.belong_id == site.id)
    if today:
        t_orders = t_orders.filter(FuelOrder.create_time >= datetime.datetime.now().date())
    t_orders = t_orders.all()
    total = len(t_orders)
    thread_nums = threads
    thread_list = []
    slice_num = total / thread_nums
    offset = 0

    def get_payment(order_tills, obj, limit=100):
        tills = ', '.join([str(i[0]) for i in order_tills])
        sql = '''select TILLITEM_PMNT_SPLIT.TILLNUM, TILLITEM_PMNT_SPLIT.PMSUBCODE from TILLITEM_PMNT_SPLIT where TILLITEM_PMNT_SPLIT.TILLNUM IN ({0})'''.format(tills)
        ib_session = init_interbase_connect(site.fuel_server)
        ib_session.execute(sql)
        res = ib_session.fetchall()
        order_tills_map = dict(order_tills)
        print(res) 
        for till_id, pmnt_subcode_id in res:
            order_id = order_tills_map.get(till_id)
            if order_id:
                order = session.query(FuelOrder).filter(FuelOrder.id == order_id).first()
                try:
                    payment_type = get_cache_payment_type(site.id, pmnt_subcode_id, site)
                    # print('----',order_id, till_id, pmnt_subcode_id, payment_type)
                    if payment_type:
                        # print('get_paytype', payment_type, pmnt_subcode_id, order_id)
                        order.payment_code = pmnt_subcode_id
                        order.payment_type = payment_type
                        order.catch_payment = True
                        try:
                            session.commit()
                            logging.info('INFO commit to db success site {0}'.format(site.name))
                        except Exception as e:
                            # logging.exception('ERROR in commit session site {0} reason {1}'.format('mf', e))
                            logging.exception('ERROR in commit session site {0} reason {1}'.format(site.name, e))
                            session.rollback()
                except Exception as e:
                    print(e)
    for i in range(thread_nums):
        if i == thread_nums + 1:
            e_offset = total
        else:
            e_offset = offset + slice_num
        print(i, offset, e_offset, slice_num) 
        t = threading.Thread(target=get_payment, args=(t_orders[offset:e_offset], FuelOrder, 50))
        offset += slice_num
        thread_list.append(t)

    for t in thread_list:
        t.start()

    for t in thread_list:
        t.join()
    print('-----end----')


def get_sup(site):
    site = get_site_by_slug(site)
    ib_session = init_interbase_connect(site.fuel_server)
    sql = '''SELECT SUPPLIERID ,SUPPLIERNAME FROM SUPPLIER'''
    ib_session.execute(sql)
    res = ib_session.fetchall()
    for itm in res:
        sid, name = itm
        name = get_clean_data(name)
        update_sup(sid, site, name=name)


def get_rev(site):
    site = get_site_by_slug(site)
    ib_session = init_interbase_connect(site.fuel_server)
    sql = '''SELECT ITEMDOCTYPE_ID ,ITEMDOCTYPE_NAME FROM ITEMDOCTYPE'''
    ib_session.execute(sql)
    res = ib_session.fetchall()
    for itm in res:
        rid, name = itm
        name = get_clean_data(name)
        update_rev(rid, site, name=name)


def get_delivery(site, start_time=None, end_time=None):
    if not start_time:
        start_time = datetime.datetime.now() - datetime.timedelta(hours=3)
        end_time = start_time + datetime.timedelta(days=1)
    st = datetime_to_string(start_time)
    et = datetime_to_string(end_time)
    site = get_site_by_slug(site)
    ib_session = init_interbase_connect(site.fuel_server)
    sql = '''Select EXTREF, pickup_date, ITEMDOCTYPE_ID, SUPPLIER_ID, TRUCK_NUMBER
From Fuel_Tank_Delivery_Header
WHERE DELIVERY_DATE BETWEEN '{0}' and '{1}'
Order By EXTREF'''.format(st, et)
    ib_session.execute(sql)
    res = ib_session.fetchall()
    for itm in res:
        _, original_create_time, rev_id, sup_id, number = itm
        number = get_clean_data(number)
        unique_str = generate_hash(_, datetime_to_string(original_create_time, '%Y-%m-%d %H:%M:%S'), unicode(rev_id),
                                   unicode(sup_id),
                                   number[2:])
        obj = get_obj_by_hash(unique_str, DeliveryRecord)
        if obj:
            continue
        rec = get_rev_by_rid(rev_id, site)
        sup = get_sup_by_sid(sup_id, site)
        if rec and sup:
            create_object(DeliveryRecord, supplier=sup.name, receiver=rec.name, truck_number=number, belong_id=site.id,
                          original_create_time=original_create_time, hash=unique_str, modify_time=original_create_time)
    update_site_status(site, '油品配送记录更新')


def get_cache_payment_type(belong_id, pmnt_subcode_id, site):
    rds = redis.Redis(db=5)
    pkey = "ptype_{}_{}".format(belong_id, pmnt_subcode_id)
    payment_type = rds.get(pkey)
    if not payment_type:
        try:
            ib_session = init_interbase_connect(site.fuel_server)
            ib_session.execute('SELECT PMNT_ID, PMSUBCODE_ID, PMNT_NAME FROM PMNT WHERE PMSUBCODE_ID={};'.format(pmnt_subcode_id))
            pmnt_id, pmsc_id, payment_type = ib_session.fetchone()
            payment_type = get_clean_data(payment_type)
            rds.setex(pkey, payment_type, 3600)
            return payment_type
        except Exception as e:
            logging.exception('can not get payment type in pmnt pmnt_subcode_id :{}, site: {}'.format(pmnt_subcode_id, site.name))
            return None
    return payment_type.decode('utf-8')


if __name__ == '__main__':
    get_fuel_order('test', datetime.datetime(2017, 1, 1), datetime.datetime(2017, 1, 2))
    # site = get_site_by_slug('test')
    # get_sup('test')
    # get_rev('test')
    # get_delivery('test', datetime.datetime(2017, 5, 1), datetime.datetime(2017, 10, 30))

