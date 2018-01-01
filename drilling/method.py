# coding: utf-8
from __future__ import unicode_literals

import math

import logging

from drilling.utils import get_goods_inventory_by_barcode
from sqlalchemy import func

from drilling.models import GoodsOrder, session, Site


def query_by_pagination(session, obj, order_by='id', start_offset=0, limit=1000):
    def get_count(q):
        count_q = q.statement.with_only_columns([func.count()]).order_by(None)
        count = q.session.execute(count_q).scalar()
        return count

    total = get_count(session.query(obj))
    total_page = int(math.ceil(total / float(limit)))
    start = 0
    if start_offset:
        start = start_offset / limit

    for i in xrange(start, total_page):
        offset = limit * i
        result = session.query(obj).filter(obj.catch_payment == False).order_by(order_by).limit(limit).offset(
            offset).all()
        logging.info(
            'Current {0}->{1}/{2} {3}%'.format(offset, offset + limit, total, float(offset + limit) / total * 100))
        yield result


def refresh_goods_gpm():
    for orders in query_by_pagination(session, GoodsOrder, limit=200):
        for order in orders:
            site = Site()
            site.id = order.belong_id
            inventory = get_goods_inventory_by_barcode(order.barcode, site)
            if not inventory.cost:
                continue
            profit = order.price - inventory.cost
            order.gpm = profit / order.price
            order.cost = inventory.cost
        session.commit()
    logging.info('INFO finish refresh goods gpm')


if __name__ == '__main__':
    refresh_goods_gpm()

