# coding: utf-8
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from api.models import GoodsOrder


class Command(BaseCommand):
    def handle(self, *args, **options):
        GoodsOrder.objects.all().delete()