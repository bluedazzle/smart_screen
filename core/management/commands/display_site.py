# coding: utf-8
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from api.models import Site


class Command(BaseCommand):
    def handle(self, *args, **options):
        res = Site.objects.all()
        for itm in res:
            print('{0},{1}'.format(itm.name, itm.slug))
