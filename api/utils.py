# coding: utf-8
from __future__ import unicode_literals

from drilling.models import session, SecondClassification, ThirdClassification, Classification


def get_fuel_type(cid):
    obj = session.query(SecondClassification).filter(SecondClassification.id == cid).first()
    return obj.name


def get_first_cls_name_by_ss_cls_ids(ids):
    cls_ids = session.query(ThirdClassification.grandparent_id).filter(ThirdClassification.id.in_(ids)).all()
    result = session.query(Classification.name).filter(Classification.id.in_(cls_ids)).all()
    return result
