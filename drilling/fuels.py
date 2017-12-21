# coding: utf-8
from __future__ import unicode_literals

import datetime

from drilling.db.interbase import init_interbase_connect
from drilling.models import session, FuelOrder, DeliveryRecord, Receiver, Supplier
from drilling.utils import get_site_by_slug, get_clean_data, get_fuel_order_by_hash, generate_hash, datetime_to_string, \
    create_fuel_order, update_sup, update_rev, get_obj_by_hash, create_object, get_object_by_id, get_rev_by_rid, \
    get_sup_by_sid, query_by_pagination


def get_fuel_order(site, start_time=None, end_time=None):
    if not start_time:
        start_time = datetime.datetime.now()
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
            break
        create_fuel_order(till_id=till_id, original_create_time=original_create_time, fuel_type=fuel_type, price=price,
                          total_price=total_price, amount=amount, pump_id=pump_id, hash=unique_str, belong_id=site.id,
                          classification_id=dept, barcode=barcode, super_cls_id=int(super_dept))
    get_fuel_order_payment(site)


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


def get_fuel_order_payment(site):
    orders = session.query(FuelOrder).filter(FuelOrder.catch_payment == False).all()
    total = len(orders)
    for orders in query_by_pagination(session, FuelOrder, total, limit=100):
        ib_session = init_interbase_connect(site.fuel_server)
        tills = ','.join([unicode(i.till_id) for i in orders])
        if not tills:
            return
        sql = '''select TILLITEM_PMNT_SPLIT.TILLNUM, TILLITEM_PMNT_SPLIT.PMSUBCODE, PMNT.PMNT_NAME from TILLITEM_PMNT_SPLIT,
    PMNT where TILLITEM_PMNT_SPLIT.TILLNUM IN ({0}) AND
    PMNT.PMSUBCODE_ID=TILLITEM_PMNT_SPLIT.PMSUBCODE'''.format(tills)
        ib_session.execute(sql)
        res = ib_session.fetchall()
        for itm in res:
            till_id, payment_code, payment_type = itm
            order = session.query(FuelOrder).filter(FuelOrder.till_id == till_id).first()
            if order:
                order.payment_code = payment_code
                order.payment_type = get_clean_data(payment_type)
                order.catch_payment = True
        session.commit()


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
        start_time = datetime.datetime.now()
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


if __name__ == '__main__':
    get_fuel_order('test', datetime.datetime(2017, 1, 1), datetime.datetime(2017, 1, 2))
    # site = get_site_by_slug('test')
    # get_sup('test')
    # get_rev('test')
    # get_delivery('test', datetime.datetime(2017, 5, 1), datetime.datetime(2017, 10, 30))
