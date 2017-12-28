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
