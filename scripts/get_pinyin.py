# coding: utf-8
import logging

import math

from sqlalchemy import func
from xpinyin import Pinyin

from drilling.models import GoodsInventory, session


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
        result = session.query(obj).order_by(order_by).limit(limit).offset(
            offset).all()
        logging.info(
            'Current {0}->{1}/{2} {3}%'.format(offset, offset + limit, total, float(offset + limit) / total * 100))
        yield result


def get_pinyin():
    p = Pinyin()
    for results in query_by_pagination(session, GoodsInventory):
        for itm in results:
            itm.py = p.get_initials(itm.name, '').replace(' ', '')
        session.commit()

if __name__ == '__main__':
    get_pinyin()