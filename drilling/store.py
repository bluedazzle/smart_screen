# coding: utf-8
from __future__ import unicode_literals

import datetime

import logging

from drilling.db.interbase import init_interbase_connect
from drilling.models import session, GoodsOrder
from drilling.utils import get_site_by_slug, datetime_to_string, get_clean_data, update_classification, \
    update_second_classification, update_third_classification, generate_hash, get_goods_order_by_hash, \
    create_fuel_order, \
    create_goods_order


def get_store_order(site, start_time=None, end_time=None):
    if not start_time:
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(days=1)
    st = datetime_to_string(start_time)
    et = datetime_to_string(end_time)
    site = get_site_by_slug(site)
    ib_session = init_interbase_connect(site.fuel_server)
    sql = '''SELECT
       TILL.SALEDATE,
       POSBATCH.POS_ID,
       TILL.TILLNUM,
       TILL.SHIFT,
       TILL.TIMECLOSE,
       ITEM.DEPT,
       ITEM.BARCODE,
       ITEM.FULLDESCRIPTION AS ITEMNAME,
       UNITSIZE.UNITNAME,
       TILLITEM.STDPRICE PRICE,
       (TILLITEM.TOTAL) AS TOTAL,
       (TILLITEM.QTY * TILLITEM.WEIGHT) AS QTY,
       (TILLITEM.QTY * TILLITEM.WEIGHT * TILLITEM.STDPRICE) AS CALC_TOTAL

FROM DAYBATCH DAYBATCH , POSBATCH, TILLITEM,TILL, ITEM  ,UNITSIZE
WHERE
 ( TILLITEM.STATUSTYPE NOT IN ( 26 )) AND
 ( TILL.STATUSTYPE NOT IN ( 26 )) AND
      (DAYBATCH.DAY_BATCH_DATE  BETWEEN '{0}' AND '{1}')
 AND  ( TILLITEM.TILLNUM = TILL.TILLNUM)
 AND  ( TILLITEM.POS_BATCH_ID = TILL.POS_BATCH_ID)
 AND  ( TILL.POS_BATCH_ID = POSBATCH.POS_BATCH_ID)
 AND  ( POSBATCH.DAY_BATCH_ID = DAYBATCH.DAY_BATCH_ID)
 AND  ( TILLITEM.PLU = ITEM.ITEMID )
 AND  ( UNITSIZE.UNITID = ITEM.BASEUNIT)
 AND  ( TILL.STATUSTYPE IN (1,2,3,4,15))
 AND  ( TILLITEM.STATUSTYPE IN (1,2,3,4,15))
 ORDER BY
TILL.TIMECLOSE DESC'''.format(st, et)
    ib_session.execute(sql)
    orders = ib_session.fetchall()
    for order in orders:
        sale_date, pos_id, till_id, shift, original_create_time, dept, barcode, name, unit, price, total, amount, _ = order
        if unicode(dept).startswith('1001'):
            continue
        name = get_clean_data(name)
        barcode = get_clean_data(barcode)
        unique_str = generate_hash(unicode(till_id), datetime_to_string(original_create_time, '%Y-%m-%d %H:%M:%S'),
                                   unicode(price), unicode(amount), unicode(barcode),
                                   unicode(total), unicode(site.id))
        res = get_goods_order_by_hash(unique_str)
        if res:
            break
        create_goods_order(till_id=till_id, original_create_time=original_create_time, classification_id=dept,
                           price=price, total=total, amount=amount, barcode=barcode, hash=unique_str, name=name,
                           belong_id=site.id)
    get_goods_order_payment(site)


def get_third_classify(site):
    site = get_site_by_slug(site)
    ib_session = init_interbase_connect(site.fuel_server)
    sql = '''select SUBDEPTID, SUBDEPTNAME, DEPTID from SUBDEPT'''
    ib_session.execute(sql)
    res = ib_session.fetchall()
    for itm in res:
        cid, name, parent_id = itm
        name = get_clean_data(name)
        update_third_classification(cid, name=name, parent_id=parent_id)


def get_second_classify(site):
    site = get_site_by_slug(site)
    ib_session = init_interbase_connect(site.fuel_server)
    sql = '''select DEPTID, DEPTNAME, SUPERDEPTID from DEPT'''
    ib_session.execute(sql)
    res = ib_session.fetchall()
    for itm in res:
        cid, name, parent_id = itm
        name = get_clean_data(name)
        update_second_classification(cid, name=name, parent_id=parent_id)


def get_first_classify(site):
    site = get_site_by_slug(site)
    ib_session = init_interbase_connect(site.fuel_server)
    sql = '''select SUPERDEPTID, SUPERDEPTNAME from SUPERDEPT'''
    ib_session.execute(sql)
    res = ib_session.fetchall()
    for itm in res:
        cid, name = itm
        try:
            name = get_clean_data(name)
            update_classification(cid, name=name)
        except Exception as e:
            logging.exception('ERROR get first classify in {0} reason {1}'.format(cid, e))
            continue


def get_goods_order_payment(site):
    orders = session.query(GoodsOrder).filter(GoodsOrder.catch_payment == False).all()
    ib_session = init_interbase_connect(site.fuel_server)
    till_list = [unicode(order.till_id) for order in orders]
    if not till_list:
        return
    tills = ','.join(till_list)
    sql = '''select TILLITEM_PMNT_SPLIT.TILLNUM, TILLITEM_PMNT_SPLIT.PMSUBCODE, PMNT.PMNT_NAME from TILLITEM_PMNT_SPLIT,
PMNT where TILLITEM_PMNT_SPLIT.TILLNUM IN ({0}) AND
PMNT.PMSUBCODE_ID=TILLITEM_PMNT_SPLIT.PMSUBCODE'''.format(tills)
    ib_session.execute(sql)
    res = ib_session.fetchall()
    for itm in res:
        till_id, payment_code, payment_type = itm
        orders = session.query(GoodsOrder).filter(GoodsOrder.till_id == till_id).all()
        for order in orders:
            order.payment_code = payment_code
            order.payment_type = get_clean_data(payment_type)
            order.catch_payment = True
        session.commit()


def get_inventories(site):
    site = get_site_by_slug(site)
    ib_session = init_interbase_connect(site.fuel_server)
    sql = '''SELECT SUPERDEPT.SUPERDEPTNAME ,
 DEPT.DEPTNAME,SUBDEPT.SUBDEPTNAME,
 ITEM.FULLDESCRIPTION,
 ITEM.ITEMCODE,UNITSIZE.UNITNAME,
 ITEM.ITEMID,
 SUM(ITEMLOCTOTAL.CALCBALANCE_QTY) as total
FROM ITEMLOCTOTAL,ITEM,SUBDEPT,DEPT,SUPERDEPT,UNITSIZE
WHERE
 (UNITSIZE.UNITID=ITEM.MANAGEUNIT)
  AND
 (SUBDEPT.SUBDEPTID=ITEM.DEPT)
  AND
 (SUBDEPT.DEPTID=DEPT.DEPTID)
  AND
 (DEPT.SUPERDEPTID=SUPERDEPT.SUPERDEPTID)
  AND
 (ITEMLOCTOTAL.ITEM_ID = ITEM.ITEMID)
GROUP BY
 SUPERDEPT.SUPERDEPTNAME,DEPT.DEPTNAME,SUBDEPT.SUBDEPTNAME,ITEM.FULLDESCRIPTION,
 ITEM.ITEMCODE,UNITSIZE.UNITNAME,ITEM.MANAGUNITFACTOR,ITEM.ITEMID
ORDER BY
  ITEM.ITEMCODE'''
    ib_session.execute(sql)
    res = ib_session.fetchall()
    for itm in res:
        print get_clean_data(itm[2]), get_clean_data(itm[3])



if __name__ == '__main__':
    # get_store_order('test', datetime.datetime(2017, 5, 2), datetime.datetime(2017, 5, 3))
    # get_first_classify('test')
    # get_second_classify('test')
    # get_third_classify('test')
    get_inventories('test')
