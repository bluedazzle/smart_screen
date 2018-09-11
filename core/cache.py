# coding: utf-8
from __future__ import unicode_literals

import redis

client_redis_zhz = None


def config_client_redis_zhz():
    global client_redis_zhz
    client_redis_zhz = redis.StrictRedis(db=1)
