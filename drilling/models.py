# coding: utf-8

from __future__ import unicode_literals

from sqlalchemy import Column, String, DateTime, Integer, Boolean, create_engine, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class FuelTank(Base):
    __tablename__ = 'api_fueltank'

    id = Column(Integer, primary_key=True)
    tank_id = Column(Integer)
    name = Column(String, default='')
    current = Column(Float, default=0.0)
    max_value = Column(Float, default=0.0)
    min_value = Column(Float, default=0.0)
    temperature = Column(Float, default=0.0)
    water_stick = Column(Float, default=0.0)
    belong_id = Column(Integer)
    create_time = Column(DateTime)
    original_create_time = Column(DateTime)


class Site(Base):
    __tablename__ = 'api_site'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    slug = Column(String)
    fuel_server = Column(String)
    bos_server = Column(String)


engine = create_engine('postgresql+psycopg2://rapospectre:123456qq@localhost:5432/smart_screen',
                       encoding='utf-8'.encode())

DBSession = sessionmaker(bind=engine)

session = DBSession()
