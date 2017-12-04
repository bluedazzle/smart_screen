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
    name = Column(String)
    current = Column(Float)
    max_value = Column(Float)
    min_value = Column(Float)
    temperature = Column(Float)
    water_stick = Column(Float)
    belong_id = Column(Integer)
    original_create_time = Column(DateTime)


engine = create_engine('postgresql+psycopg2://postgres:123456qq@localhost:5432/smart_screen',
                       encoding='utf-8'.encode())

DBSession = sessionmaker(bind=engine)

session = DBSession()
