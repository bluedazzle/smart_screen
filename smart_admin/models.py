# coding: utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser
from django.db import models

# Create your models here.
from api.models import Site


class Account(AbstractBaseUser):
    name = models.CharField(max_length=128, unique=True)
    forbid = models.BooleanField(default=False)
    token = models.CharField(max_length=64, unique=True)
    belong = models.ForeignKey(Site, related_name='site_accounts')

    USERNAME_FIELD = ['name']

    def __unicode__(self):
        return '{0}-{1}'.format(self.belong.name, self.name)


class Excel(models.Model):
    belong = models.ForeignKey(Site, related_name='site_excels')
    year = models.IntegerField(default=2018)
    month = models.IntegerField(default=1)

    gas_sell_cost_u = models.FloatField(default=0.0)
    diesel_sell_cost_v = models.FloatField(default=0.0)
    daily_repair_ad = models.FloatField(default=0.0)
    oil_loss_ai = models.FloatField(default=0.0)
    goods_sell_cost_bi = models.FloatField(default=0.0)
    depreciation_cost_ao = models.FloatField(default=0.0)
    salary_cost_ao = models.FloatField(default=0.0)
    water_ele_cost_af = models.FloatField(default=0.0)
    other_cost_aq = models.FloatField(default=0.0)
    oil_gross_profit_w = models.FloatField(default=0.0)
    total_profit_gaddi = models.FloatField(default=0.0)
    oil_profit_g = models.FloatField(default=0.0)
    goods_profit_i = models.FloatField(default=0.0)
    ton_oil_g_profit_wdivn = models.FloatField(default=0.0)
    ton_gas_g_profit_xdivo = models.FloatField(default=0.0)
    per_oil_amount_m = models.FloatField(default=0.0)
    ton_die_g_profit_ydivp = models.FloatField(default=0.0)
    ton_oil_cost_aadivn = models.FloatField(default=0.0)
    ton_oil_profit_j = models.FloatField(default=0.0)
    daliy_sell_amount_l = models.FloatField(default=0.0)

    def __unicode__(self):
        return '{0}: {1}年-{2}月'.format(self.belong.name, self.year, self.month)
