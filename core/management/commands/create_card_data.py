# coding: utf-8
from __future__ import unicode_literals

import datetime
import random

from django.core.management.base import BaseCommand

from api.models import CardRecord, AbnormalRecord, Site


class Command(BaseCommand):
    def handle(self, *args, **options):
        site = Site.objects.filter(slug='test')[0]
        cr = CardRecord()
        cr.classification_id = 100101
        cr.card_id = '111'
        cr.card_type = 1
        cr.balance = 10000
        cr.total = 1000
        cr.belong_id = 1
        cr.belong = site
        cr.unique_id = random.randint(10, 1000)
        cr.original_create_time = datetime.datetime.now()
        cr.save()

        cr = CardRecord()
        cr.classification_id = 100102
        cr.card_id = '112'
        cr.card_type = 2
        cr.balance = 20000
        cr.total = 2000
        cr.belong_id = 1
        cr.belong = site
        cr.unique_id = random.randint(10, 1000)
        cr.original_create_time = datetime.datetime.now()
        cr.save()

        cr = CardRecord()
        cr.classification_id = 100101
        cr.card_id = ''
        cr.bank_unique_id = '1234'
        cr.bank_card_id = '636'
        cr.card_type = 1
        cr.balance = 10000
        cr.total = 1000
        cr.belong_id = 1
        cr.unique_id = random.randint(10, 1000)
        cr.belong = site
        cr.original_create_time = datetime.datetime.now()
        cr.save()

        ar = AbnormalRecord()
        ar.belong = site
        ar.card_type = 1
        ar.card_id = '111'
        ar.abnormal_type = 1
        ar.reason = '单日汽油消费 800 元以上'
        ar.start_time = datetime.datetime.now()
        ar.end_time = datetime.datetime(2018, 3, 1)
        ar.save()

        ar = AbnormalRecord()
        ar.belong = site
        ar.card_type = 2
        ar.card_id = '112'
        ar.abnormal_type = 2
        ar.reason = '一周内汽柴油混刷'
        ar.start_time = datetime.datetime.now()
        ar.end_time = datetime.datetime(2018, 3, 1)
        ar.save()
