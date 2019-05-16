# coding: utf-8
from __future__ import unicode_literals

from drilling.store import get_goods_order_payment
from drilling.models import Site, session

from core.util import conf

from drilling.db.session import config_oil_session

import logging

logging.getLogger().setLevel(logging.INFO)

config_oil_session(conf)


def init_site_data():
    result = session.query(Site).filter(Site.check == True).all()
    return result


def get_payments():
    sites = init_site_data()
    for site in sites:
        get_goods_order_payment(site, 4)


if __name__ == '__main__':
    get_payments()

