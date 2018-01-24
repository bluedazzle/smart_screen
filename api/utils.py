# coding: utf-8
from __future__ import unicode_literals

from drilling.models import session, SecondClassification, ThirdClassification, Classification


def get_fuel_type(cid):
    obj = session.query(SecondClassification).filter(SecondClassification.id == cid).first()
    if obj:
        return obj.name
    return None


def get_first_cls_name_by_ss_cls_ids(ids):
    cls_ids = session.query(ThirdClassification.grandparent_id).filter(ThirdClassification.id.in_(ids)).all()
    result = session.query(Classification.name).filter(Classification.id.in_(cls_ids)).all()
    return result


def get_first_cls_name_by_id(cid):
    res = session.query(Classification.name).filter(Classification.id == cid).first()
    if res:
        return res[0]
    return None


def get_all_super_cls_id():
    res = session.query(Classification.id).all()
    return [itm[0] for itm in res]


def get_all_goods_super_cls_id():
    res = get_all_super_cls_id()
    res = [itm for itm in res if 2000 <= itm <= 2999]
    return res


def get_card_type(card_type_id):
    card_dict = {0: '银行卡',
                 1: '记名卡',
                 2: '车队卡'}
    return card_dict.get(card_type_id, '记名卡')