# coding: utf-8
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from api.models import AbnormalRecord


class Command(BaseCommand):
    def handle(self, *args, **options):
        res = AbnormalRecord.objects.filter(reason='一周内汽柴油混刷').all()
        res.delete()
