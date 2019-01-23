# coding: utf-8
from __future__ import unicode_literals

import datetime

import logging
import threading

from drilling.db.interbase import init_interbase_connect
from drilling.models import session, GoodsOrder
from drilling.utils import get_site_by_slug, datetime_to_string, get_clean_data, update_classification, \
    update_second_classification, update_third_classification, generate_hash, get_goods_order_by_hash, \
    create_fuel_order, \
    create_goods_order, update_goods_inventory, get_goods_inventory_by_barcode, add_timezone_to_naive_time, \
    query_by_pagination, get_py, update_site_status


def get_store_order(site, start_time=None, end_time=None):
    if not start_time:
        start_time = datetime.datetime.now() - datetime.timedelta(hours=3)
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
    nums = 0
    for order in orders:
        sale_date, pos_id, till_id, shift, original_create_time, dept, barcode, name, unit, price, total, amount, _ = order
        dept_str = unicode(dept)
        if dept_str.startswith('1001'):
            continue
        name = get_clean_data(name)
        barcode = get_clean_data(barcode)
        unique_str = generate_hash(unicode(till_id), datetime_to_string(original_create_time, '%Y-%m-%d %H:%M:%S'),
                                   unicode(price), unicode(amount), unicode(barcode),
                                   unicode(total), unicode(site.id))
        res = get_goods_order_by_hash(unique_str)
        if res:
            continue
        create_goods_order(till_id=till_id, original_create_time=original_create_time, classification_id=dept,
                           price=price, total=total, amount=amount, barcode=barcode, hash=unique_str, name=name,
                           belong_id=site.id, super_cls_id=int(dept_str[:4]))
        nums += 1
        gi = get_goods_inventory_by_barcode(barcode, site)
        if gi:
            gi.last_sell_time = add_timezone_to_naive_time(original_create_time)
            try:
                session.commit()
            except Exception as e:
                logging.exception('ERROR in commit session site {0} reason {1}'.format(site.name, e))
                session.rollback()
    logging.info('=============create store order {0} site {1}=============='.format(nums, site.name))
    # get_goods_order_payment(site)
    update_site_status(site, '商品订单更新')


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


def get_goods_order_payment(site, threads=2, today=False):
    t_orders = session.query(GoodsOrder).filter(GoodsOrder.catch_payment == False,
                                                GoodsOrder.belong_id == site.id)
    if today:
        t_orders = t_orders.filter(GoodsOrder.create_time == datetime.datetime.now().date())
    t_orders = t_orders.all()
    total = len(t_orders)
    thread_nums = threads
    thread_list = []
    slice_num = total / thread_nums
    offset = 0

    def get_payment(thread_name, obj, start_offset=0, end_offset=0, limit=100):
        for orders in query_by_pagination(site, session, obj, total, start_offset=start_offset, end_offset=end_offset,
                                          limit=limit,
                                          name=thread_name):
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
            try:
                session.flush()
                session.commit()
                logging.info('INFO commit to db success site {0}'.format(site.name))
            except Exception as e:
                logging.exception('ERROR in commit session site {0} reason {1}'.format(site.name, e))
                session.rollback()

    for i in range(thread_nums):
        if i == thread_nums + 1:
            e_offset = total
        else:
            e_offset = offset + slice_num
        t = threading.Thread(target=get_payment, args=(i, GoodsOrder, offset, e_offset, 100))
        offset += slice_num
        thread_list.append(t)

    for t in thread_list:
        t.start()

    for t in thread_list:
        t.join()


def get_inventories(site):
    site = get_site_by_slug(site)
    ib_session = init_interbase_connect(site.fuel_server)
    sql = '''SELECT SUPERDEPT.SUPERDEPTID,
 DEPT.DEPTID,
 SUBDEPT.SUBDEPTID,
 ITEM.BARCODE,
 ITEM.FULLDESCRIPTION,
 ITEM.ITEMCODE,
 UNITSIZE.UNITNAME,
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
 SUPERDEPT.SUPERDEPTID,DEPT.DEPTID,SUBDEPT.SUBDEPTID,ITEM.FULLDESCRIPTION,ITEM.BARCODE,
 ITEM.ITEMCODE,UNITSIZE.UNITNAME,ITEM.MANAGUNITFACTOR,ITEM.ITEMID
ORDER BY
  ITEM.ITEMCODE'''
    ib_session.execute(sql)
    res = ib_session.fetchall()
    total = len(res)
    for itm in res:
        f_cls, s_cls, t_cls, barcode, name, itemcode, unit, itemid, amount = itm
        barcode = get_clean_data(barcode)
        name = get_clean_data(name)
        unit = get_clean_data(unit)
        unique_str = generate_hash(unicode(f_cls), unicode(s_cls), unicode(t_cls), barcode, unicode(site.id))
        update_goods_inventory(unique_str, name=name, unit=unit, hash=unique_str, barcode=barcode, itemcode=barcode,
                               third_cls_id=t_cls, py=get_py(name),
                               second_cls_id=s_cls, cls_id=f_cls, amount=amount, belong_id=site.id)
    logging.info('SUCCESS update goods inventory total {0}'.format(total))
    update_site_status(site, '商品库存更新')


if __name__ == '__main__':
    # get_store_order('test', datetime.datetime(2017, 8, 2), datetime.datetime(2017, 8, 3))
    # get_first_classify('test')
    # get_second_classify('test')
    # get_third_classify('test')
    get_inventories('test')
