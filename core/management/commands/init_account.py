# coding: utf-8
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from api.models import Site
from smart_admin.models import Account


class Command(BaseCommand):
    def handle(self, *args, **options):
        sites = Site.objects.all()
        for site in sites:
            name = site.slug
            if Account.objects.filter(name=name).exists():
                print 'account {0} exist'.format(name)
                continue
            account = Account(name=name)
            account.set_password('123')
            account.belong = site
            account.token = name
            account.save()
            print 'create account succcess!'
