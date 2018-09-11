# coding: utf-8
from __future__ import unicode_literals

import logging
import codecs
import math

from sqlalchemy import func
from xpinyin import Pinyin

from drilling.models import Site, session


def get_site_from_csv():
    p = Pinyin()

    with codecs.open('ip.csv', encoding='utf-8') as f1:
        for line in f1:
            name, fuel, bos = line.split(',')
            site = Site()
            site.name = name
            site.fuel_server = fuel
            site.bos_server = bos
            site.slug = p.get_initials(name, '').replace(' ', '')
            session.add(site)
        session.commit()


if __name__ == '__main__':
    get_site_from_csv()
