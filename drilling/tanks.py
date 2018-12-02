# coding: utf-8
from __future__ import unicode_literals

import logging

import copy

import datetime

from drilling.db.interbase import init_interbase_connect
from drilling.db.session import with_session
from drilling.models import session
from drilling.utils import get_site_by_slug, get_tank_by_tank_id, add_timezone_to_naive_time, get_all_tanks_by_site, \
    get_clean_data, create_record, generate_hash, get_record_by_hash, get_latest_settlement_record, datetime_to_string, \
    update_site_status


def get_tank_value(site):
    site = get_site_by_slug(site)
    ib_session = init_interbase_connect(site.fuel_server)
    for tank_id in range(1, 10):
        sql = 'SELECT SHIFT_CONTROL_ID ,TANK_ID ,WATER_STICK ,CLOSE_QTY ,WATER_VOLUME ,TRANS_DATE FROM FUEL_TANK_READING WHERE TANK_ID = {0} ORDER BY TRANS_DATE DESC'.format(
            tank_id)
        ib_session.execute(sql)
        res = ib_session.fetchone()
        if not res:
            logging.info('{0}：no value result for site {1} tank {2}'.format('get_tank_value', site.name, tank_id))
            break
        tank = get_tank_by_tank_id(tank_id, site.id)
        tank.current = res[3] if res[3] else 0
        tank.original_create_time = add_timezone_to_naive_time(res[-1])
        logging.info('INFO read value for site {0} tank {1} success'.format(site.name, tank_id))
    try:
        session.commit()
    except Exception as e:
        logging.exception('ERROR in commit session site {0} reason {1}'.format(site.name, e))
        session.rollback()
    update_site_status(site, '油库读数更新成功')


def get_tank_temperature(site):
    site = get_site_by_slug(site)
    ib_session = init_interbase_connect(site.fuel_server)
    for tank_id in range(1, 10):
        # sql = 'SELECT FDT.TEMPERATURE,FDT.READ_TIME, FT.TANK_ID, FT.TANK_NAME FROM FUEL_DAY_TEMPERATURE FDT, FUEL_TANKS FT WHERE FT.TANK_ID = {0} ORDER BY FDT.READ_TIME DESC'.format(
        sql = 'SELECT TEMPERATURE, READ_TIME FROM FUEL_DAY_TEMPERATURE where TANK_ID = {0} order by READ_TIME DESC'.format(
            tank_id)
        ib_session.execute(sql)
        res = ib_session.fetchone()
        if not res:
            logging.info(
                '{0}：no temperature result for site {1} tank {2}'.format('get_tank_temperature', site.name, tank_id))
            break
        tank = get_tank_by_tank_id(tank_id, site.id)
        tank.temperature = res[0]
        tank.original_create_time = add_timezone_to_naive_time(res[1])
        logging.info('INFO read temperature for site {0} tank {1} success'.format(site.name, tank_id))
    try:
        session.commit()
    except Exception as e:
        logging.exception('ERROR in commit session site {0} reason {1}'.format(site.name, e))
        session.rollback()
    update_site_status(site, '油库温度更新成功')


def get_tank_info(site):
    site = get_site_by_slug(site)
    ib_session = init_interbase_connect(site.fuel_server)
    sql = 'SELECT TANK_ID ,TANK_NAME ,VOLUME_QTY ,ALARM_QTY, GRADE_PLU FROM FUEL_TANKS'
    ib_session.execute(sql)
    res = ib_session.fetchall()
    for itm in res:
        tank_id, tank_name, max_value, min_value, grade_id = itm
        tank_name = tank_name.strip().decode('gbk')
        obj = get_tank_by_tank_id(itm[0], site.id, tank_id=tank_id, name=tank_name, max_value=max_value,
                                  min_value=min_value, grade_id=grade_id)
        obj.max_value = max_value
        obj.min_value = min_value
        obj.grade_id = grade_id
    try:
        session.commit()
    except Exception as e:
        logging.exception('ERROR in commit session site {0} reason {1}'.format(site.name, e))
        session.rollback()
    update_site_status(site, '油库基本信息更新成功')


def get_tank_grade(site):
    site = get_site_by_slug(site)
    tanks = get_all_tanks_by_site(site)
    ib_session = init_interbase_connect(site.fuel_server)
    for tank in tanks:
        if not tank.grade_id:
            continue
        sql = 'SELECT GRADE, GRADENAME FROM FUELGRADE WHERE GRADE={0}'.format(tank.grade_id)
        ib_session.execute(sql)
        res = ib_session.fetchone()
        if not res:
            continue
        grade, grade_name = res
        tank.name = get_clean_data(grade_name)
        logging.info(
            'INFO read tank fuel type for site {0} tank {1} success, new fuel: {2}'.format(site.name, tank.tank_id,
                                                                                           tank.name))
    try:
        session.commit()
    except Exception as e:
        logging.exception('ERROR in commit session site {0} reason {1}'.format(site.name, e))
        session.rollback()
    update_site_status(site, '油库种类更新成功')


def get_inventory_record(site, start_time=None, end_time=None):
    if not start_time:
        start_time = datetime.datetime.now() - datetime.timedelta(hours=3)
        end_time = start_time + datetime.timedelta(days=1)
    st = datetime_to_string(start_time)
    et = datetime_to_string(end_time)
    site = get_site_by_slug(site)
    sql = '''SELECT FTR.TANK_ID,
FS.SHIFT_END ACTIVITY_TIME,
3 ACTIVITY_TYPE,
CAST(NULL AS VARCHAR(20)) EXTREF,
CAST(NULL AS DOUBLE PRECISION) ORIGINAL_VOLUME,
CAST(NULL AS DOUBLE PRECISION) RECEIVING_VOLUME,
FTR.GROSS_STICK,
FTR.WATER_STICK,
FTR.CLOSE_QTY FUEL_VOLUME,
FTR.TANK_TEMP FUEL_TEMP,
FTR.DENSITY FUEL_DENSITY,
FTR.DENSITY_15 FUEL_DENSITY_STD,
FTR.CLOSE_VOLUME_15 FUEL_VOLUME_STD,
FTR.SHIFT_CONTROL_ID,
FS.SHIFT_START SHIFT_START,
FTR.MANUAL_TEMPERATURE_1 AS ENV_TEMP
FROM FUEL_SHIFT_CONTROL FS, DAYBATCH DB, FUEL_TANK_READING FTR
WHERE FTR.SHIFT_CONTROL_ID = FS.SHIFT_CONTROL_ID
AND FS.DAY_BATCH_ID = DB.DAY_BATCH_ID
AND DB.DAY_BATCH_DATE BETWEEN '{start_time}' AND '{end_time}'
AND NOT (FS.SHIFT_END IS NULL)
UNION
/* 2 - readings on end delivery */
SELECT FTD.TANK_ID,
FTD.DELIVERY_END_TIME,
2,
FTH.EXTREF,
COMPAREINT(FTH.ITEMDOCTYPE_ID, 11, '=') * (- FTDD.INVOICE_VOLUME_15) +
COMPAREINT(FTH.ITEMDOCTYPE_ID, 11, '<>') * FTDD.INVOICE_VOLUME_15,
FTD.DELIVERY_VOLUME,
FTD.END_GROSS_STICK,
FTD.END_WATER_STICK,
FTD.END_VOLUME,
FTD.END_TANK_TEMPERATURE,
FTD.END_TANK_DENSITY,
FTD.END_TANK_DENSITY_15,
FTD.END_TANK_VOLUME_15,
FTH.SHIFT_CONTROL_ID,
FS.SHIFT_START SHIFT_START ,
FTD.ENV_TEMPERATURE
FROM FUEL_SHIFT_CONTROL FS, DAYBATCH DB, FUEL_TANK_DELIVERY FTD,
FUEL_TANK_DELIVERY_HEADER FTH, FUEL_TANK_DELIVERY_DOCUMENT FTDD
WHERE FTD.SHIFT_CONTROL_ID = FS.SHIFT_CONTROL_ID
AND FS.DAY_BATCH_ID = DB.DAY_BATCH_ID
AND FTH.SERNUM = FTD.HEADERID
AND FTH.SERNUM = FTDD.HEADERID
AND FTDD.TANK_ID = FTD.TANK_ID
AND FTDD.TRUCK_TANK_ID = FTD.TRUCK_TANK_ID
AND FTH.STATUS in( 'A','C')
AND DB.DAY_BATCH_DATE BETWEEN '{start_time}' AND '{end_time}'
AND FTH.ITEMDOCTYPE_ID IN (1, 7, 8, 10, 11)
UNION
/* 1 - readings on start delivery */
SELECT FTD.TANK_ID,
FTD.DELIVERY_DATE,
1,
FTH.EXTREF,
CAST(NULL AS DOUBLE PRECISION),
CAST(NULL AS DOUBLE PRECISION),
FTD.START_GROSS_STICK,
FTD.WATER_STICK,
FTD.START_VOLUME,
FTD.TANK_TEMPERATURE,
FTD.START_TANK_DENSITY,
FTD.START_TANK_DENSITY_15,
FTD.START_VOLUME_15,
FTH.SHIFT_CONTROL_ID,
FS.SHIFT_START SHIFT_START ,
CAST(20 AS DOUBLE PRECISION)
FROM FUEL_SHIFT_CONTROL FS, DAYBATCH DB, FUEL_TANK_DELIVERY FTD,
FUEL_TANK_DELIVERY_HEADER FTH
WHERE FTD.SHIFT_CONTROL_ID = FS.SHIFT_CONTROL_ID
AND FS.DAY_BATCH_ID = DB.DAY_BATCH_ID
AND FTH.SERNUM = FTD.HEADERID
AND FTH.STATUS in( 'A','C')
AND DB.DAY_BATCH_DATE BETWEEN '{start_time}' AND '{end_time}'
AND FTH.ITEMDOCTYPE_ID IN (1, 7, 8, 10, 11)'''.format(start_time=st, end_time=et)
    ib_session = init_interbase_connect(site.fuel_server)
    ib_session.execute(sql)
    records = ib_session.fetchall()
    record_obj_list = []
    tank = get_tank_by_tank_id(1, site.id)
    previous_record = get_latest_settlement_record(tank.id)
    if previous_record:
        volum_sum = previous_record.fuel_standard_volum
    else:
        volum_sum = 0
    for record in records:
        tank_id, original_create_time, record_type, extref, send_amount, receive_amount, altitude, water_altitude, fuel_volum, fuel_temperature, experiment_density, standard_density, fuel_standard_volum, shift_control_id, start_time, experiment_temperature = record
        unique_str = generate_hash(unicode(tank_id), unicode(record_type), unicode(fuel_volum),
                                   unicode(fuel_temperature), unicode(experiment_density),
                                   unicode(standard_density), unicode(fuel_standard_volum), unicode(shift_control_id))
        exist = get_record_by_hash(unique_str)
        if exist:
            if exist.record_type == 3:
                previous_record = exist
                volum_sum = previous_record.fuel_standard_volum
            elif exist.record_type == 2:
                volum_sum = volum_sum + exist.receive_amount
            continue
        if tank.tank_id != tank_id:
            tank = get_tank_by_tank_id(tank_id, site.id)
            previous_record = get_latest_settlement_record(tank.id)
            if previous_record:
                volum_sum = previous_record.fuel_standard_volum
            else:
                volum_sum = 0
        obj = create_record(tank_id=tank.id, original_create_time=original_create_time, record_type=record_type,
                            send_amount=send_amount, receive_amount=receive_amount, fuel_volum=fuel_volum,
                            fuel_temperature=fuel_temperature, experiment_density=experiment_density,
                            standard_density=standard_density, fuel_standard_volum=fuel_standard_volum,
                            shift_control_id=shift_control_id, hash=unique_str, belong_id=site.id,
                            experiment_temperature=experiment_temperature, altitude=altitude,
                            water_altitude=water_altitude, fuel_name=tank.name)
        if obj.record_type == 3:
            obj.tank_out_amount = volum_sum - fuel_standard_volum
            volum_sum = obj.fuel_standard_volum
        elif obj.record_type == 2:
            volum_sum = volum_sum + receive_amount
        obj_dict = {'record': obj, 'tank_id': tank_id}
        record_obj_list.append(copy.copy(obj_dict))
    try:
        session.commit()
    except Exception as e:
        logging.exception('ERROR in commit session site {0} reason {1}'.format(site.name, e))
        session.rollback()
    for data in record_obj_list:
        record = data.get('record')
        tank_id = data.get('tank_id')
        if not (record or tank_id):
            continue
        if record.record_type == 1:
            continue
        if record.record_type == 2:
            record.loss_amount = record.receive_amount - record.send_amount
            continue
        sql = '''SELECT SUM((isinlist(FPR.authorization_type, 'E') * FPR.CLOSE_METER +
isinlist(FPR.authorization_type, 'M') * FPR.MANUAL_CLOSE_VOLUME) -
(isinlist(FPH.authorization_type, 'E') * FPR.OPEN_METER + isinlist(FPH.authorization_type, 'M') *
FPR.MANUAL_OPEN_VOLUME)) TOTAL
FROM FUEL_PUMP_READING FPR, FUEL_PUMPS_HOSE FPH
WHERE FPH.PUMP_ID = FPR.PUMP_ID
AND FPH.HOSE_ID = FPR.HOSE_ID
AND FPR.SHIFT_CONTROL_ID = {0}
AND FPH.TANK1_ID = {1}'''.format(record.shift_control_id, tank_id)
        ib_session.execute(sql)
        totals = ib_session.fetchall()

        def total_add(x, y):
            if y[0]:
                return x + y[0]
            return x

        if totals:
            total = reduce(total_add, totals, 0)
            record.tanker_act_out_amount = total
        if record.record_type == 3:
            record.loss_amount = record.tanker_act_out_amount - record.tank_out_amount
        logging.info('INFO update record {0: %Y-%m-%d %H:%M:%S} success!'.format(record.original_create_time))
        try:
            session.commit()
        except Exception as e:
            logging.exception('ERROR in commit session site {0} reason {1}'.format(site.name, e))
            session.rollback()
    update_site_status(site, '班结记录更新成功')


if __name__ == '__main__':
    # get_tank_value('test')
    # get_tank_info('test')
    get_tank_temperature('test')
    # get_inventory_record('test', datetime.datetime(2017, 1, 6), datetime.datetime(2017, 1, 8))
    # get_tank_info('test')
    # get_tank_grade('test')
    # get_inventory_before()
