# coding: utf-8
from __future__ import unicode_literals

import fdb

INTERBASE_USER = 'sysdba'
INTERBASE_SECRET = 'masterkey'


def init_interbase_connect(host='47.104.103.166'):
    con = fdb.connect(host=host, port=3050, database='C:/Office/Db/OFFICE.GDB', user=INTERBASE_USER,
                      password=INTERBASE_SECRET, sql_dialect=1)
    session = con.cursor()
    return session
