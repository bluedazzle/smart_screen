# coding: utf-8
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from api.models import Site
from smart_admin.models import Account


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-n', '--name', type=str)
        parser.add_argument('-p', '--pwd', type=str)
        parser.add_argument('-s', '--site', type=str)

    def handle(self, *args, **options):
        name = options.get('name')
        password = options.get('pwd')
        site = options.get('site')
        try:
            site = Site.objects.get(slug=site)
        except Exception as e:
            print '站点{0}不存在'.format(site)
            return
        if Account.objects.filter(name=name).exists():
            print '账号 {0} 已存在'.format(name)
            return
        account = Account(name=name)
        account.set_password(password)
        account.belong = site
        account.save()
        print '创建账号成功！'
