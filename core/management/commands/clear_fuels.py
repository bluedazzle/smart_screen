# coding: utf-8
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from api.models import FuelOrder


class Command(BaseCommand):
    def handle(self, *args, **options):
        itms = FuelOrder.objects.all()
        for itm in itms:
            itm.delete()


