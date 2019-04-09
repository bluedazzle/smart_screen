# coding: utf-8
import pytz

import fdb
from drilling.models import session, FuelTank


def get_tank():
    # con = fdb.connect(host='47.104.103.166', port=3050, database='C:/Office/Db/OFFICE.GDB', user='sysdba',
    con = fdb.connect(host='47.104.103.166', port=3050, database='C:/Office/Db/OFFICE.GDB', user='sysdba',
                      password='masterkey', sql_dialect=1)
    cur = con.cursor()
    # cur.execute('SELECT * FROM FUEL_TANKS ORDER BY TANK_ID DESC ROWS 2 TO 10')
    cur.execute(
        'SELECT SHIFT_CONTROL_ID ,TANK_ID ,WATER_STICK ,CLOSE_QTY ,WATER_VOLUME ,TRANS_DATE FROM FUEL_TANK_READING WHERE TANK_ID = 2 ORDER BY TRANS_DATE DESC')
    res = cur.fetchone()
    print(res)

    # tank = session.query(FuelTank).filter(FuelTank.tank_id == 1).first()
    # tank.current = res[3]
    # tank.original_create_time = res[-1].replace(tzinfo=pytz.timezone('Asia/Shanghai'))
    # session.commit()

get_tank()
