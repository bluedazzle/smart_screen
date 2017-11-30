# coding: utf-8
from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils import timezone


# Create your models here.

class BaseModel(models.Model):
    create_time = models.DateTimeField(default=timezone.now)
    modify_time = models.DateTimeField(auto_now=True)
    original_create_time = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class Site(BaseModel):
    name = models.CharField(max_length=40, default='')
    slug = models.CharField(max_length=10, unique=True)
    fuel_server = models.GenericIPAddressField()
    bos_server = models.GenericIPAddressField()

    def __unicode__(self):
        return self.name


class FuelOrder(BaseModel):
    fuel_choices = (
        (1, '95号汽油'),
        (2, '97号汽油'),
        (3, '0号柴油'),
    )

    fuel_type = models.IntegerField(default=1, choices=fuel_choices)
    amount = models.FloatField(default=0.0)  # 卖出数量
    total_price = models.FloatField(default=0.0)
    payment_type = models.IntegerField(default=1)
    belong = models.ForeignKey(Site, related_name='site_fuel_orders')

    def __unicode__(self):
        return self.total_price


class GoodsOrder(BaseModel):
    name = models.CharField(max_length=120, default='')
    price = models.FloatField(default=0.0)
    payment_type = models.IntegerField(default=1)
    goods_type = models.IntegerField(default=1)
    belong = models.ForeignKey(Site, related_name='site_goods_orders')

    def __unicode__(self):
        return self.name


class FuelTank(BaseModel):
    tank_id = models.IntegerField(default=1)
    name = models.CharField(max_length=30, default='', null=True, blank=True)
    current = models.FloatField(default=0.0)
    max_value = models.FloatField(default=10000.0)
    min_value = models.FloatField(default=1000.0)
    temperature = models.FloatField(default=0.0)
    water_stick = models.FloatField(default=0.0)
    belong = models.ForeignKey(Site, related_name='site_fuel_tanks')

    def __unicode__(self):
        return self.name


class InventoryRecord(BaseModel):
    record_choices = (
        (1, '班结日结'),
    )

    record_type = models.IntegerField(default=1, choices=record_choices)
    # 油品进货
    send_amount = models.FloatField(default=0.0)
    receive_amount = models.FloatField(default=0.0)
    # 油品付出
    tank_out_amount = models.FloatField(default=0.0)
    tanker_out_amount = models.FloatField(default=0.0)
    loss_amount = models.FloatField(default=0.0)

    tank_amount = models.FloatField(default=0.0)
    tank = models.ForeignKey(FuelTank, related_name='tank_inventory_records')
    belong = models.ForeignKey(Site, related_name='site_inventory_records')

    def __unicode__(self):
        return '{0}-{1}-{2}'.format(self.belong.name, self.tank.name, self.record_type)
