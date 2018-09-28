# coding: utf-8
from __future__ import unicode_literals

import codecs
import random

from drilling.utils import get_now_time_with_timezone
from xpinyin import Pinyin

from drilling.models import Site, session

from core.util import conf

from drilling.db.session import config_oil_session

config_oil_session(conf)


def get_site_from_csv():
    p = Pinyin()
    now = get_now_time_with_timezone()
    py_list = []
    with codecs.open('ip.csv', encoding='utf-8') as f1:
        for line in f1:
            name, bos, fuel = line.split(',')
            py = p.get_initials(name, '').replace(' ', '')
            if py in py_list:
                py = '{0}{1}'.format(py, random.randint(0, 100))
            py_list.append(py)
            site = Site()
            site.name = name
            site.fuel_server = fuel.strip()
            site.bos_server = bos.strip()
            site.slug = py
            site.create_time = now
            site.modify_time = now
            site.original_create_time = now
            site.check = False
            site.lock = 1000
            session.add(site)
        session.commit()


if __name__ == '__main__':
    get_site_from_csv()
