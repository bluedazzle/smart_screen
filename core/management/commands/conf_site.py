# coding: utf-8
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from api.models import Site


class Command(BaseCommand):
    def handle(self, *args, **options):
        sites = Site.objects.all()
        for site in sites:
            site.password = 123
            site.lock = 1000
            site.save()
