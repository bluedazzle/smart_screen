# coding: utf-8
from __future__ import unicode_literals

from drilling.models import Site, session
from drilling.tasks import init_task
from core.util import conf

from drilling.db.session import config_oil_session

config_oil_session(conf)


def main():
    site_list = session.query(Site).filter(Site.check == True).all()
    for site in site_list:
        init_task.delay(site.slug)


if __name__ == '__main__':
    # print check_fuel('10.97.226.97')
    # print check_eps('10.97.226.98')
    main()

