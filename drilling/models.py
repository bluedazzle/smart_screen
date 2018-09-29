# coding: utf-8

from __future__ import unicode_literals

from drilling.db.session import OilSession
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
    classification_id = Column(Integer)
    super_cls_id = Column(Integer)
    barcode = Column(String)

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
    super_cls_id = Column(Integer)
    hash = Column(String)
    total = Column(Float)
    cost = Column(Float)
    gpm = Column(Float)
    amount = Column(Float)

    def __init__(self, *args, **kwargs):
        self.payment_type = '其他'
        self.cost = 0.0
        self.gpm = 0.0
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
    belong_id = Column(Integer)
    create_time = Column(DateTime)
    modify_time = Column(DateTime)
    original_create_time = Column(DateTime)
    hash = Column(String)


class GoodsInventory(Base):
    __tablename__ = 'api_goodsinventory'

    id = Column(Integer, primary_key=True)
    belong_id = Column(Integer)
    create_time = Column(DateTime)
    modify_time = Column(DateTime)
    last_sell_time = Column(DateTime)
    original_create_time = Column(DateTime)
    hash = Column(String)
    third_cls_id = Column(Integer)
    second_cls_id = Column(Integer)
    cls_id = Column(Integer)
    name = Column(String)
    barcode = Column(String)
    itemcode = Column(String)
    py = Column(String)
    unit = Column(String)
    amount = Column(Float)
    cost = Column(Float)

    def __init__(self, *args, **kwargs):
        self.cost = 0.0
        super(GoodsInventory, self).__init__(*args, **kwargs)


class CardRecord(Base):
    __tablename__ = 'api_cardrecord'

    id = Column(Integer, primary_key=True)
    belong_id = Column(Integer)
    create_time = Column(DateTime)
    modify_time = Column(DateTime)
    original_create_time = Column(DateTime)
    unique_id = Column(String)
    parent_id = Column(String)
    card_id = Column(String)
    bank_card_id = Column(String)
    detail = Column(String)
    pump_id = Column(Integer)
    balance = Column(Float)
    total = Column(Float)
    card_type = Column(Integer)
    classification = Column(String)
    eps_unique_id = Column(String)


class AbnormalRecord(Base):
    __tablename__ = 'api_abnormalrecord'

    id = Column(Integer, primary_key=True)
    belong_id = Column(Integer)
    create_time = Column(DateTime)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    card_id = Column(String)
    card_type = Column(Integer)
    reason = Column(String)
    abnormal_type = Column(Integer)


class Site(Base):
    __tablename__ = 'api_site'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    slug = Column(String)
    fuel_server = Column(String)
    bos_server = Column(String)
    check = Column(Boolean)
    create_time = Column(DateTime)
    modify_time = Column(DateTime)
    original_create_time = Column(DateTime)
    lock = Column(Integer)

    depreciation_cost = Column(Float, default=0.0)
    members = Column(Integer, default=0)
    salary_cost = Column(Float, default=0.0)
    daily_repair = Column(Float, default=0.0)
    water_ele_cost = Column(Float, default=0.0)
    oil_loss = Column(Float, default=0.0)
    other_cost = Column(Float, default=0.0)
    total_cost = Column(Float, default=0.0)
    oil_gross_profit = Column(Float, default=0.0)
    oil_profit = Column(Float, default=0.0)
    goods_profit = Column(Float, default=0.0)
    total_profit = Column(Float, default=0.0)
    ton_oil_cost = Column(Float, default=0.0)
    ton_oil_g_profit = Column(Float, default=0.0)
    per_oil_amount = Column(Float, default=0.0)
    per_profit = Column(Float, default=0.0)
    per_goods_income = Column(Float, default=0.0)

    gas_92 = Column(Float, default=0.0)
    gas_95 = Column(Float, default=0.0)
    gas_98 = Column(Float, default=0.0)
    die_35 = Column(Float, default=0.0)
    die_20 = Column(Float, default=0.0)
    die_10 = Column(Float, default=0.0)
    die_0 = Column(Float, default=0.0)
    die_d20 = Column(Float, default=0.0)


class CeleryLog(Base):
    __tablename__ = 'super_admin_celerylog'

    id = Column(Integer, primary_key=True)
    create_time = Column(DateTime)
    modify_time = Column(DateTime)
    original_create_time = Column(DateTime)
    task_id = Column(String)
    status = Column(Integer)
    task_type = Column(Integer)
    err_info = Column(String)
    belong_id = Column(Integer)


class Task(Base):
    __tablename__ = 'super_admin_task'

    id = Column(Integer, primary_key=True)
    create_time = Column(DateTime)
    modify_time = Column(DateTime)
    original_create_time = Column(DateTime)
    task_id = Column(String)
    name = Column(String)
    belong_id = Column(Integer)


class Excel(Base):
    __tablename__ = 'smart_admin_excel'

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    month = Column(Integer)
    belong_id = Column(Integer)
    gas_sell_cost_u = Column(Float)
    diesel_sell_cost_v = Column(Float)
    daily_repair_ad = Column(Float)
    oil_loss_ai = Column(Float)
    goods_sell_cost_bi = Column(Float)
    depreciation_cost_ao = Column(Float)
    salary_cost_ao = Column(Float)
    water_ele_cost_af = Column(Float)
    other_cost_aq = Column(Float)
    oil_gross_profit_w = Column(Float)
    total_profit_gaddi = Column(Float)
    oil_profit_g = Column(Float)
    goods_profit_i = Column(Float)
    ton_oil_g_profit_wdivn = Column(Float)
    ton_gas_g_profit_xdivo = Column(Float)
    per_oil_amount_m = Column(Float)
    ton_die_g_profit_ydivp = Column(Float)
    ton_oil_cost_aadivn = Column(Float)
    ton_oil_profit_j = Column(Float)
    daliy_sell_amount_l = Column(Float)


# engine = create_engine('postgresql+psycopg2://rapospectre:123456qq@localhost:5432/ss_06',
#                        encoding='utf-8'.encode())
#
# DBSession = sessionmaker(bind=engine, autoflush=False)

session = OilSession
