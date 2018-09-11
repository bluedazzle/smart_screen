# coding: utf-8
from __future__ import unicode_literals

import logging

from drilling.db.interbase import init_interbase_connect
from drilling.db.mysql import init_mysql_connect
from drilling.models import Site, session


def check_fuel(ip):
    try:
        ib_session = init_interbase_connect(ip)
        sql = 'SELECT TANK_ID ,TANK_NAME ,VOLUME_QTY ,ALARM_QTY, GRADE_PLU FROM FUEL_TANKS'
        ib_session.execute(sql)
        res = ib_session.fetchall()
        if res:
            return res
        return False
    except Exception as e:
        return False


def check_eps(ip):
    try:
        ms_session = init_mysql_connect(ip)
        res = ms_session.execute('select * from tbl_epstrade limit 10').fetchall()
        if res:
            return res
        return False
    except Exception as e:
        return False


def check_site():
    site_list = session.query(Site).filter(Site.check == False).all()
    for site in site_list:
        if check_fuel(site.fuel_server) and check_eps(site.bos_server):
            logging.info('check site {0} success'.format(site.name))
            site.check = True
        else:
            logging.info('check site {0} failed'.format(site.name))
    session.commit()


if __name__ == '__main__':
    print check_fuel('10.97.226.98')
    print check_eps('10.97.226.97')
    # check_site()
