# coding: utf-8
from __future__ import unicode_literals

from drilling.fuels import get_fuel_order_payment
from drilling.models import Site, session

from core.util import conf

from drilling.db.session import config_oil_session

config_oil_session(conf)

import logging

logging.getLogger().setLevel(logging.INFO)


def init_site_data():
    result = session.query(Site).filter(Site.check == True).all()
    return result


def get_payments():
    sites = init_site_data()
    for site in sites:
        get_fuel_order_payment(site, 4)


if __name__ == '__main__':
    get_payments()

