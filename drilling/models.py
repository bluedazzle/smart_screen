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
    grade_id = Column(Integer)
    name = Column(String, default='')
    current = Column(Float, default=0.0)
    max_value = Column(Float, default=0.0)
    min_value = Column(Float, default=0.0)
    temperature = Column(Float, default=0.0)
    water_stick = Column(Float, default=0.0)
    belong_id = Column(Integer)
    create_time = Column(DateTime)
    original_create_time = Column(DateTime)


class InventoryRecord(Base):
    __tablename__ = 'api_inventoryrecord'

    id = Column(Integer, primary_key=True)
    fuel_name = Column(String)
    record_type = Column(Integer)
    send_amount = Column(Float, default=0.0)
    receive_amount = Column(Float, default=0.0)
    tank_out_amount = Column(Float, default=0.0)
    tanker_out_amount = Column(Float, default=0.0)
    tanker_act_out_amount = Column(Float, default=0.0)
    back_tank_amount = Column(Float, default=0.0)
    loss_amount = Column(Float, default=0.0)
    water_altitude = Column(Float, default=0.0)
    altitude = Column(Float, default=0.0)
    fuel_volum = Column(Float, default=0.0)
    fuel_temperature = Column(Float, default=0.0)
    fuel_standard_volum = Column(Float, default=0.0)
    experiment_temperature = Column(Float, default=0.0)
    experiment_density = Column(Float, default=0.0)
    standard_temperature = Column(Float, default=0.0)
    standard_density = Column(Float, default=0.0)
    vcf20 = Column(Float, default=0.0)
    shift_control_id = Column(Integer, default=0.0)
    hash = Column(String)
    tank_id = Column(Integer)
    belong_id = Column(Integer)
    create_time = Column(DateTime)
    original_create_time = Column(DateTime)


class FuelOrder(Base):
    __tablename__ = 'api_fuelorder'

    id = Column(Integer, primary_key=True)
    fuel_type = Column(String)
    amount = Column(Float)
    price = Column(Float)
    total_price = Column(Float)
    payment_type = Column(String)
    payment_code = Column(Integer)
    till_id = Column(Integer)
    pump_id = Column(Integer)
    belong_id = Column(Integer)
    create_time = Column(DateTime)
    original_create_time = Column(DateTime)
    catch_payment = Column(Boolean)
    hash = Column(String)

    def __init__(self, *args, **kwargs):
        self.payment_type = '其他'
        self.catch_payment = False
        self.payment_code = 0
        super(FuelOrder, self).__init__(*args, **kwargs)


class Classification(Base):
    __tablename__ = 'api_classification'

    id = Column(Integer, primary_key=True)
    create_time = Column(DateTime)
    original_create_time = Column(DateTime)
    belong_id = Column(Integer)

    name = Column(String)


class SecondClassification(Base):
    __tablename__ = 'api_secondclassification'

    id = Column(Integer, primary_key=True)
    create_time = Column(DateTime)
    original_create_time = Column(DateTime)
    belong_id = Column(Integer)

    name = Column(String)
    parent_id = Column(Integer)


class ThirdClassification(Base):
    __tablename__ = 'api_thirdclassification'

    id = Column(Integer, primary_key=True)
    create_time = Column(DateTime)
    original_create_time = Column(DateTime)
    belong_id = Column(Integer)

    name = Column(String)
    parent_id = Column(Integer)
    grandparent_id = Column(Integer)


class GoodsOrder(Base):
    __tablename__ = 'api_goodsorder'

    id = Column(Integer, primary_key=True)
    create_time = Column(DateTime)
    original_create_time = Column(DateTime)
    belong_id = Column(Integer)

    name = Column(String)
    barcode = Column(String)
    price = Column(Float)
    payment_type = Column(String)
    payment_code = Column(Integer)
    catch_payment = Column(Boolean)
    till_id = Column(Integer)
    classification_id = Column(Integer)
    hash = Column(String)
    total = Column(Float)
    amount = Column(Float)

    def __init__(self, *args, **kwargs):
        self.payment_type = '其他'
        self.catch_payment = False
        self.payment_code = 0
        super(GoodsOrder, self).__init__(*args, **kwargs)


class Supplier(Base):
    __tablename__ = 'api_supplier'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    sid = Column(Integer)
    belong_id = Column(Integer)


class Receiver(Base):
    __tablename__ = 'api_receiver'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    rid = Column(Integer)
    belong_id = Column(Integer)


class DeliveryRecord(Base):
    __tablename__ = 'api_deliveryrecord'

    id = Column(Integer, primary_key=True)
    supplier = Column(String)
    receiver = Column(String)
    truck_number = Column(String)
    belong_id = Column(String)
    create_time = Column(DateTime)
    modify_time = Column(DateTime)
    original_create_time = Column(DateTime)
    hash = Column(String)


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
