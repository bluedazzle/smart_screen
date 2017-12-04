# coding: utf-8
from __future__ import unicode_literals

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, DateTime, create_engine

Base = declarative_base()
engine = create_engine("mysql+pymysql://eps:gd^&*<>?eps@localhost:3306/eps", echo=True)
session = sessionmaker(bind=engine)
session = session()
print session.execute('select * from tbl_eft;').fetchall()
