# coding: utf-8
from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils import timezone


# Create your models here.

class BaseModel(models.Model):
    create_time = models.DateTimeField(default=timezone.now)
    modify_time = models.DateTimeField(auto_now=True)
    original_create_time = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        abstract = True


class Site(BaseModel):
    name = models.CharField(max_length=40, default='')
    slug = models.CharField(max_length=10, unique=True)
    # office 系统
    fuel_server = models.GenericIPAddressField()
    # eps 系统
    bos_server = models.GenericIPAddressField()
    password = models.CharField(max_length=120, null=True, blank=True)
    pictures = models.TextField(default='', null=True, blank=True)
    info = models.TextField(default='', null=True, blank=True)
    lock = models.IntegerField(default=60)

    def __unicode__(self):
        return self.name


class Classification(BaseModel):
    name = models.CharField(max_length=100, default='')
    id = models.IntegerField(unique=True, primary_key=True)
    belong = models.ForeignKey(Site, related_name='site_classification', null=True, blank=True)

    def __unicode__(self):
        return '{0}-{1}'.format(self.id, self.name)


class SecondClassification(BaseModel):
    name = models.CharField(max_length=100, default='')
    id = models.IntegerField(unique=True, primary_key=True)
    parent = models.ForeignKey(Classification, related_name='cls_sub_cls')
    belong = models.ForeignKey(Site, related_name='site_second_classification', null=True, blank=True)

    def __unicode__(self):
        return '{0}-{1}<-{2}'.format(self.id, self.name, self.parent.name)


class ThirdClassification(BaseModel):
    name = models.CharField(max_length=100, default='')
    id = models.IntegerField(unique=True, primary_key=True)
    parent = models.ForeignKey(SecondClassification, related_name='sub_cls_ssub_cls')
    grandparent = models.ForeignKey(Classification, related_name='cls_ssub_cls')
    belong = models.ForeignKey(Site, related_name='site_third_classification', null=True, blank=True)

    def __unicode__(self):
        return '{0}-{1}<-{2}<-{3}'.format(self.id, self.name, self.parent.name, self.grandparent.name)


class FuelOrder(BaseModel):
    fuel_type = models.CharField(default='', max_length=50)
    amount = models.FloatField(default=0.0)  # 卖出数量
    price = models.FloatField(default=0.0)
    total_price = models.FloatField(default=0.0)
    payment_type = models.CharField(default='其他', max_length=20)
    payment_code = models.IntegerField(default=0)
    catch_payment = models.BooleanField(default=False)
    till_id = models.IntegerField(default=0)
    pump_id = models.IntegerField(default=0)
    hash = models.CharField(max_length=64, unique=True)
    classification = models.ForeignKey(ThirdClassification, related_name='ssub_cls_fuels')
    super_cls = models.ForeignKey(SecondClassification, related_name='sub_cls_fuels')
    barcode = models.CharField(max_length=100, default='', null=True, blank=True)
    belong = models.ForeignKey(Site, related_name='site_fuel_orders')

    def __unicode__(self):
        return '{0}-{1: %Y-%m-%d %H:%M:%S}-{2}-{3}L-￥{4}'.format(self.belong.name, self.original_create_time,
                                                                 self.fuel_type, self.amount, self.total_price)


class GoodsInventory(BaseModel):
    name = models.CharField(max_length=200, default='')
    py = models.CharField(max_length=80, null=True, blank=True)
    barcode = models.CharField(max_length=100, default='', null=True, blank=True)
    itemcode = models.CharField(max_length=100, null=True, blank=True)
    unit = models.CharField(max_length=20, null=True, blank=True)
    amount = models.FloatField(default=0.0)
    cost = models.FloatField(default=0.0)
    hash = models.CharField(max_length=128, unique=True)
    last_sell_time = models.DateTimeField()

    third_cls = models.ForeignKey(ThirdClassification, related_name='third_cls_gis')
    second_cls = models.ForeignKey(SecondClassification, related_name='second_cls_gis')
    cls = models.ForeignKey(Classification, related_name='cls_gis')
    belong = models.ForeignKey(Site, related_name='site_gis')

    def __unicode__(self):
        return '{0}: {1} {2}{3}'.format(self.belong.name, self.name, self.amount, self.unit)


class GoodsOrder(BaseModel):
    name = models.CharField(max_length=120, default='')
    barcode = models.CharField(max_length=50, default='')
    price = models.FloatField(default=0.0)
    amount = models.FloatField(default=0)
    total = models.FloatField(default=0.0)
    payment_type = models.CharField(default='其他', max_length=20)
    payment_code = models.IntegerField(default=0)
    catch_payment = models.BooleanField(default=False)
    till_id = models.IntegerField(default=0)
    classification = models.ForeignKey(ThirdClassification, related_name='ssub_cls_goods')
    super_cls = models.ForeignKey(Classification, related_name='cls_goods', null=True, blank=True,
                                  on_delete=models.SET_NULL)
    gpm = models.FloatField(default=0.0)
    cost = models.FloatField(default=0.0)
    hash = models.CharField(max_length=64, unique=True)
    belong = models.ForeignKey(Site, related_name='site_goods_orders')

    def __unicode__(self):
        return '{0}-{1}x{2} {3}元-{4: %Y-%m-%d %H:%M:%S}'.format(self.belong.name, self.name, self.amount, self.total,
                                                                self.original_create_time)


class FuelTank(BaseModel):
    tank_id = models.IntegerField(default=1)
    grade_id = models.IntegerField(default=1, null=True, blank=True)
    name = models.CharField(max_length=30, default='', null=True, blank=True)
    current = models.FloatField(default=0.0, null=True, blank=True)
    max_value = models.FloatField(default=10000.0, null=True, blank=True)
    min_value = models.FloatField(default=1000.0, null=True, blank=True)
    temperature = models.FloatField(default=0.0, null=True, blank=True)
    water_stick = models.FloatField(default=0.0, null=True, blank=True)
    belong = models.ForeignKey(Site, related_name='site_fuel_tanks')

    def __unicode__(self):
        return self.name


class InventoryRecord(BaseModel):
    record_choices = (
        (1, '卸前计量'),
        (2, '卸后计量'),
        (3, '班结计量'),
    )

    record_type = models.IntegerField(default=1, choices=record_choices)
    # 油品进货
    send_amount = models.FloatField(default=0.0, null=True, blank=True)
    receive_amount = models.FloatField(default=0.0, null=True, blank=True)
    # 油品付出
    tank_out_amount = models.FloatField(default=0.0, null=True, blank=True)
    # 加油机发出量
    tanker_out_amount = models.FloatField(default=0.0, null=True, blank=True)
    # 加油机实出量
    tanker_act_out_amount = models.FloatField(default=0.0, null=True, blank=True)
    # 回罐数量
    back_tank_amount = models.FloatField(default=0.0, null=True, blank=True)
    # 损耗量
    loss_amount = models.FloatField(default=0.0, null=True, blank=True)

    # 水高
    water_altitude = models.FloatField(default=0.0, null=True, blank=True)
    # 油水总高
    altitude = models.FloatField(default=0.0, null=True, blank=True)
    # 油品体积
    fuel_volum = models.FloatField(default=0.0, null=True, blank=True)
    # 油温
    fuel_temperature = models.FloatField(default=0.0, null=True, blank=True)
    # 油品标准体积
    fuel_standard_volum = models.FloatField(default=0.0, null=True, blank=True)
    # 实验
    experiment_temperature = models.FloatField(default=0.0, null=True, blank=True)
    experiment_density = models.FloatField(default=0.0, null=True, blank=True)
    # 标准
    standard_temperature = models.FloatField(default=0.0, null=True, blank=True)
    standard_density = models.FloatField(default=0.0, null=True, blank=True)

    vcf20 = models.FloatField(default=1.0, null=True, blank=True)
    shift_control_id = models.IntegerField(default=1, null=True, blank=True)
    hash = models.CharField(max_length=64, unique=True)

    fuel_name = models.CharField(max_length=50, default='', null=True, blank=True)
    tank = models.ForeignKey(FuelTank, related_name='tank_inventory_records')
    belong = models.ForeignKey(Site, related_name='site_inventory_records')

    def __unicode__(self):
        return '{0}-{1}号油罐-{2}-{3}-{4: %Y-%m-%d %H:%M:%S}'.format(self.belong.name, self.tank.tank_id, self.tank.name,
                                                                  self.record_type, self.original_create_time)


class DeliveryRecord(BaseModel):
    supplier = models.CharField(default='', max_length=50)
    receiver = models.CharField(default='', max_length=50)
    truck_number = models.CharField(default='', max_length=30)
    hash = models.CharField(max_length=128, unique=True)
    belong = models.ForeignKey(Site, related_name='site_deliveries')

    def __unicode__(self):
        return '{0}-{1: %Y-%m-%d %H:%M:%S}-{2}'.format(self.belong.name, self.original_create_time, self.truck_number)


class Supplier(models.Model):
    sid = models.IntegerField(default=1)
    name = models.CharField(default='', max_length=50)
    belong = models.ForeignKey(Site, related_name='site_suppliers')

    def __unicode__(self):
        return '{0}-{1}'.format(self.belong.name, self.name)


class Receiver(models.Model):
    rid = models.IntegerField(default=1)
    name = models.CharField(default='', max_length=50)
    belong = models.ForeignKey(Site, related_name='site_receivers')

    def __unicode__(self):
        return '{0}-{1}'.format(self.belong.name, self.name)


class FuelPlan(models.Model):
    year = models.IntegerField(default=2018)
    fuel_type = models.ForeignKey(SecondClassification, related_name='cls_plans')
    jan = models.FloatField(default=0)
    feb = models.FloatField(default=0)
    mar = models.FloatField(default=0)
    apr = models.FloatField(default=0)
    may = models.FloatField(default=0)
    jun = models.FloatField(default=0)
    jul = models.FloatField(default=0)
    aug = models.FloatField(default=0)
    sep = models.FloatField(default=0)
    oct = models.FloatField(default=0)
    nov = models.FloatField(default=0)
    dec = models.FloatField(default=0)
    total = models.FloatField(default=0)
    belong = models.ForeignKey(Site, related_name='site_plans', null=True, blank=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return '{0}-{1}'.format(self.year, self.fuel_type.name)


class CardRecord(BaseModel):
    card_type_choices = (
        (0, '银行卡'),
        (1, '记名|不记名卡'),
        (2, '车队卡'),
    )

    unique_id = models.IntegerField(unique=True)
    # eps id
    parent_id = models.IntegerField()
    card_id = models.CharField(max_length=128, null=True, blank=True)
    bank_card_id = models.CharField(max_length=128, null=True, blank=True)
    # 银行流水
    eps_unique_id = models.CharField(max_length=128, null=True, blank=True)
    pump_id = models.IntegerField(default=0)
    balance = models.FloatField(default=0.0)
    # 实扣金额
    total = models.FloatField(default=0.0)
    card_type = models.IntegerField(default=0, choices=card_type_choices)
    classification = models.CharField(max_length='50', null=True, blank=True)
    detail = models.CharField(max_length=50, null=True, blank=True)
    belong = models.ForeignKey(Site, related_name='site_card_records')

    def __unicode__(self):
        if self.card_type == 1 or self.card_type == 2:
            card_id = self.card_id
        else:
            card_id = self.bank_card_id
        return '{0}-{1}: ￥{2}元-{3:%Y-%m-%d %H:%M:%S}'.format(self.belong.name, card_id, self.total / 100.0,
                                                             self.original_create_time)


class AbnormalRecord(models.Model):
    card_type_choices = (
        (1, '记名|不记名卡'),
        (2, '车队卡'),
    )

    abnormal_type_choices = (
        (1, '日异常'),
        (2, '周异常')
    )

    card_id = models.CharField(max_length=128)
    card_type = models.IntegerField(default=1, choices=card_type_choices)
    reason = models.CharField(max_length=256, default='', null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    create_time = models.DateTimeField(default=timezone.now)
    abnormal_type = models.IntegerField(default=1)
    belong = models.ForeignKey(Site, related_name='site_abnormal_records')

    def __unicode__(self):
        return '{0}-{1}-{2}-{3: %Y-%m-%d %H:%M:%S}~{4: %Y-%m-%d %H:%M:%S}'.format(self.belong.name, self.card_id,
                                                                                  self.reason, self.start_time,
                                                                                  self.end_time)
