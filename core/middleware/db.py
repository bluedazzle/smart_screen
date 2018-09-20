# coding: utf-8
from __future__ import unicode_literals

from drilling.db.session import OilSession


class DBSessionMiddleware(object):
    def process_exception(self, request, exception):
        OilSession.remove()

    def process_response(self, request, response):
        OilSession.remove()
        return response
