# coding: utf-8
from __future__ import unicode_literals

import datetime

from drilling.db.interbase import init_interbase_connect
from drilling.store import get_goods_order_payment, get_store_order
from drilling.models import Site, session, GoodsOrder

from core.util import conf

from drilling.db.session import config_oil_session

import logging

logging.getLogger().setLevel(logging.INFO)

config_oil_session(conf)


def init_site_data():
    result = session.query(Site).fliter(Site.check == True).all()
    return result


def get_payments():
    sites = init_site_data()
    for site in sites:
        get_goods_order_payment(site, 4)


def test():
    get_store_order('mf', datetime.datetime(2018, 9, 25), datetime.datetime(2018, 10, 25))

if __name__ == '__main__':
    test()
