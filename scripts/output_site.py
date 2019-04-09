# coding: utf-8
from __future__ import unicode_literals

from drilling.models import Site, session


def output_site():
    sites = session.query(Site).filter(Site.check == False).all()
    for site in sites:
        print('{0},{1},{2},{3},{4}'.format(site.name, site.slug, site.fuel_server, site.bos_server, site.check))


if __name__ == '__main__':
    output_site()
