# coding:utf-8
from __future__ import unicode_literals

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def init_mysql_connect(host=''):
    engine = create_engine("mysql+pymysql://eps:gd^&*<>?eps@{0}:3306/eps".format(host), echo=True)
    session = sessionmaker(bind=engine)
    session = session()
    return session
