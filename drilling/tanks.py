# coding: utf-8
from __future__ import unicode_literals

import logging

from drilling.db.interbase import init_interbase_connect
from drilling.models import session
from drilling.utils import get_site_by_slug, get_tank_by_tank_id, add_timezone_to_naive_time


# def get_tank_temperature(site):
def get_tank_value(site):
    site = get_site_by_slug(site)
    ib_session = init_interbase_connect()
    for tank_id in range(1, 10):
        sql = 'SELECT SHIFT_CONTROL_ID ,TANK_ID ,WATER_STICK ,CLOSE_QTY ,WATER_VOLUME ,TRANS_DATE FROM FUEL_TANK_READING WHERE TANK_ID = {0} ORDER BY TRANS_DATE DESC'.format(
            tank_id)
        ib_session.execute(sql)
        res = ib_session.fetchone()
        if not res:
            logging.info('{0}：no result for site {1} tank {2}'.format('get_tank_temperature', site.name, tank_id))
            break
        tank = get_tank_by_tank_id(tank_id, site.id)
        tank.current = res[3]
        tank.original_create_time = add_timezone_to_naive_time(res[-1])
        logging.info('INFO read value for site {0} tank {1} success'.format(site.name, tank_id))
    session.commit()


# def get_tank_
# sql = 'SELECT FDT.TEMPERATURE,FDT.READ_TIME, FT.TANK_ID, FT.TANK_NAME FROM FUEL_DAY_TEMPERATURE FDT, FUEL_TANKS FT WHERE FT.TANK_ID = FDT.TANK_ID'

def get_tank_info(site):
    site = get_site_by_slug(site)
    ib_session = init_interbase_connect()
    sql = 'SELECT TANK_ID ,TANK_NAME ,VOLUME_QTY ,ALARM_QTY FROM FUEL_TANKS'
    ib_session.execute(sql)
    res = ib_session.fetchall()
    for itm in res:
        tank_id, tank_name, max_value, min_value = itm
        tank_name = tank_name.strip().decode('gbk')
        obj = get_tank_by_tank_id(itm[0], site.id, tank_id=tank_id, name=tank_name, max_value=max_value,
                                  min_value=min_value)
        obj.name = tank_name
        obj.max_value = max_value
        obj.min_value = min_value
    session.commit()


# get_tank_value('test')
get_tank_info('test')
