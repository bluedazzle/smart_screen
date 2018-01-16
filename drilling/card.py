# coding: utf-8
from __future__ import unicode_literals

import datetime

import logging

from drilling.db.interbase import init_interbase_connect
from drilling.db.mysql import init_mysql_connect, init_test
from sqlalchemy import func

from drilling.models import session, CardRecord
from drilling.utils import get_today_st_et, get_today_night, get_week_st_et, create_abnormal_record, datetime_to_string, \
    get_site_by_slug, check_card_record, create_card_record


def abnormal_card_check(card_id):
    if not card_id:
        return 0, ''
    st, et = get_today_st_et()
    card_sql = session.query(CardRecord).filter(CardRecord.card_id == unicode(card_id))
    day_card_res = card_sql.filter(CardRecord.original_create_time.between(st, et))
    # 日异常判断:
    count = day_card_res.count()
    if count > 3:
        return 1, '单日刷卡三次以上'
    day = day_card_res.filter(CardRecord.total >= 80000, CardRecord.classification == '汽油')
    count = day.count()
    if count > 0:
        return 1, '单笔汽油消费 800 元以上'
    net, nst = get_today_night()
    day_card_res = day_card_res.filter(CardRecord.original_create_time.between(st, net),
                                       CardRecord.original_create_time.between(nst, et))
    count = day_card_res.count()
    if count >= 3:
        return 1, '单日深夜刷卡三次及以上'
    # 周异常判断:
    st, et = get_week_st_et()
    week_card_res = card_sql.filter(CardRecord.original_create_time.between(st, et))
    week = week_card_res.filter(CardRecord.total >= 200000, CardRecord.classification == '汽油')
    count = week.count()
    if count > 0:
        return 2, '一周内汽油消费2000元及以上'
    week = week_card_res.filter(CardRecord.total >= 1000000, CardRecord.classification == '柴油')
    count = week.count()
    if count > 0:
        return 2, '一周内柴油消费10000元及以上'
    mix = session.query(CardRecord.classification, func.count(1)).filter(
        CardRecord.classification.in_(('汽油', '柴油')),
        CardRecord.original_create_time.between(st, et)).group_by(
        CardRecord.classification).all()
    if len(mix) < 2:
        return 0, ''
    if mix[0][1] > 0 and mix[1][1] > 0:
        return 2, '一周内汽柴油混刷'
    return 0, ''


def convert_oil_id(oil_id):
    if not oil_id:
        return '', ''
    mapping = {300314: "98号 车用汽油(Ⅲ)",
               300451: "97号 车用汽油(沪Ⅳ)",
               300061: "97号 车用汽油(Ⅲ)",
               300060: "93号 车用汽油(Ⅲ)",
               300450: "93号 车用汽油(沪Ⅳ)",
               300453: "-10号 车用柴油(沪Ⅳ)",
               300059: "90号 车用汽油(Ⅲ)",
               300454: "90号 车用汽油(沪Ⅳ)",
               300007: "93号 车用乙醇汽油",
               300011: "97号 车用汽油(II)",
               300014: "97号 车用乙醇汽油",
               300035: "-10号 车用柴油(京Ⅲ)",
               300000: "90号 车用汽油(II)",
               300003: "90号 车用乙醇汽油",
               300004: "93号 车用汽油(II)",
               300036: "-20号 轻柴油",
               300038: "-35号 轻柴油",
               300034: "-10号 轻柴油",
               300032: "0号 轻柴油",
               300033: "0号 车用柴油(京Ⅲ)",
               300037: "-20号 车用柴油(京Ⅲ)",
               300237: "-30号 轻柴油",
               300470: "-20号 车用柴油(Ⅲ)",
               300471: "-10号 车用柴油(Ⅲ)",
               300472: "0号 车用柴油(Ⅲ)",
               300062: "90号 车用汽油(京Ⅳ)",
               300077: "-35号 车用柴油(京Ⅳ)",
               300074: "0号 车用柴油(京Ⅳ)",
               300076: "-20号 车用柴油(京Ⅳ)",
               300075: "-10号 车用柴油(京Ⅳ)",
               300063: "93号 车用汽油(京Ⅳ)",
               300401: "-30号 车用柴油(京Ⅳ)",
               300426: "90号 车用乙醇汽油调合组分油(Ⅱ)",
               300465: "90号 车用乙醇汽油调合组分油(Ⅲ)",
               300425: "93号 车用乙醇汽油调合组分油(Ⅱ)",
               300466: "93号 车用乙醇汽油调合组分油(Ⅲ)",
               300048: "-50号 轻柴油",
               300064: "97号 车用汽油(京Ⅳ)",
               300467: "97号 车用乙醇汽油调合组分油(Ⅲ)",
               300474: "97号 车用乙醇汽油调合组分油(Ⅱ)",
               300409: "10号 车用柴油(京Ⅳ)",
               300028: "10号 轻柴油",
               300045: "-5号 柴油",
               300521: "0号 车用柴油(粤Ⅳ)",
               300520: "90号 车用汽油(粤Ⅳ)",
               300517: "93号 车用汽油(粤IV)",
               300518: "97号 车用汽油(粤Ⅳ)",
               300070: "-20号 车用柴油",
               300068: "0号 车用柴油",
               300069: "-10号 车用柴油",
               300071: "-35号 车用柴油",
               300475: "93号 车用甲醇汽油(M15)",
               300476: "93号 车用甲醇汽油(M5)",
               300030: "5号 轻柴油",
               300473: "5号 车用柴油(Ⅲ)",
               300073: "5号 车用柴油(京Ⅳ)",
               300535: "0号 B5调和燃料",
               300452: "0号 车用柴油(沪Ⅳ)",
               300566: "0号 普通柴油",
               300570: "5号 普通柴油",
               300550: "-35号 车用柴油(Ⅲ)",
               300072: "-50号 车用柴油",
               300565: "-35号 普通柴油",
               300568: "-10号 普通柴油",
               300567: "-20号 普通柴油",
               300574: "98号 车用汽油(粤IV)",
               300582: "-50号 车用柴油(Ⅲ)",
               300590: "93号 车用汽油(Ⅳ)",
               300591: "97号 车用汽油(Ⅳ)",
               300585: "92号 车用汽油(京Ⅴ)",
               300586: "95号 车用汽油(京Ⅴ)",
               300603: "0号 车用柴油(京Ⅴ)",
               300602: "-10号 车用柴油(京Ⅴ)",
               300601: "-20号 车用柴油(京Ⅴ)",
               300600: "-35号 车用柴油(京Ⅴ)",
               300536: "S50号 柴油机燃料调合用生物柴油BD100",
               300027: "煤油",
               300042: "-50号 军用柴油",
               300581: "-50号 普通柴油",
               300575: "-30号 普通柴油",
               300031: "5号 车用柴油(京Ⅲ)",
               300569: "10号 普通柴油",
               300641: "92号 车用汽油(沪Ⅴ)",
               300640: "95号 车用汽油(沪Ⅴ)",
               300644: "0号 车用柴油(Ⅴ)",
               300647: "92号 车用汽油(苏Ⅴ)",
               300648: "95号 车用汽油(苏Ⅴ)",
               300645: "-10号 车用柴油(Ⅴ)",
               300652: "0号 车用柴油(Ⅳ)",
               300650: "93号 车用乙醇汽油调合组分油(Ⅳ)",
               300656: "93号 车用乙醇汽油(E10) GB18351-2013",
               300654: "97号 车用乙醇汽油调合组分油(Ⅳ)",
               300657: "97号 车用乙醇汽油(E10) GB18351-2013",
               300649: "90号 车用汽油(Ⅳ)",
               300651: "-10号 车用柴油(Ⅳ)",
               300653: "98号 车用汽油(Ⅳ)",
               300668: "92号 车用汽油(Ⅴ)",
               300667: "95号 车用汽油(Ⅴ)",
               300684: "98号 车用汽油(V)",
               300646: "-20号 车用柴油(Ⅴ)",
               300690: "-35号 车用柴油(Ⅳ)",
               300694: "-20号 车用柴油(Ⅳ)",
               300693: "5号 车用柴油(Ⅳ)",
               300697: "-50号 车用柴油(Ⅳ)",
               300710: "M20车用甲醇汽油",
               300732: "92号 车用乙醇汽油(E10)(Ⅴ)",
               300734: "98号 车用乙醇汽油(E10)(Ⅴ)",
               300735: "95号 车用乙醇汽油(E10)(Ⅴ)",
               300695: "-35号 车用柴油(Ⅴ)",
               402092: "船用燃料油",
               300696: "5号 车用柴油(Ⅴ)",
               300757: "98号 车用汽油(京Ⅴ)",
               300050: "船用燃料油(DMC)",
               402097: "船用燃料油 DMC",
               300772: "-10号 车用柴油(京Ⅵ)",
               300771: "0号 车用柴油(京Ⅵ)",
               300770: "5号 车用柴油(京Ⅵ)",
               300773: "-20号 车用柴油(京Ⅵ)",
               300774: "-35号 车用柴油(京Ⅵ)",
               300775: "92号 车用汽油(京Ⅵ)",
               300776: "95号 车用汽油(京Ⅵ)",
               300777: "98号 车用汽油(京Ⅵ)",
               300767: "-50号 车用柴油(Ⅴ)",
               300258: "LNG 液化天然气",
               300338: "CNG 压缩天然气 立方",
               300738: "95号 车用乙醇汽油调合组分油(Ⅴ)",
               300731: "92号 车用乙醇汽油调合组分油(Ⅴ)",
               300339: "CNG 压缩天然气 千克",
               300669: "89号 车用汽油(Ⅴ)",
               300736: "89号 车用乙醇汽油(E10)(Ⅴ)",
               300739: "89号 车用乙醇汽油调和组分油(Ⅴ)",
               300861: "-35号 车用柴油(Ⅵ)",
               300867: "95号 车用汽油(ⅥA)",
               300862: "-20号 车用柴油(Ⅵ)",
               300863: "0号 车用柴油(Ⅵ)",
               300864: "-10号 车用柴油(Ⅵ)",
               300865: "92号 车用汽油(ⅥA)",
               300866: "98号 车用汽油(ⅥA)",
               300879: "92号 车用乙醇汽油调合组分油(ⅥA)",
               300877: "92号 车用乙醇汽油(E10)(ⅥA)",
               300880: "95号 车用乙醇汽油调合组分油(ⅥA)",
               300878: "95号 车用乙醇汽油(E10)(ⅥA)",
               300889: "98号 车用乙醇汽油(E10)(ⅥA)"}
    try:
        oil_id = int(oil_id)
    except Exception as e:
        logging.exception('ERROR in convert oil id {0}'.format(e))
        return '', ''
    oil_str = mapping.get(oil_id, '其他')
    if '柴油' in oil_str:
        return oil_str, '柴油'
    if '汽油' in oil_str:
        return oil_str, '汽油'
    return oil_str, oil_str


def convert_goods(good_id):
    if not good_id:
        return '', ''
    mapping = {2010: "饼干/糕点",
               2011: "面包",
               2012: "速食",
               2014: "清洁用品",
               2004: "奶类",
               2005: "酒类",
               2013: "日用品",
               2015: "个人护理用品",
               1001: "燃料油",
               1002: "石油气体",
               2001: "香烟",
               2002: "包装饮料",
               2003: "散装饮料",
               2006: "糖果",
               2007: "零食",
               2008: "家庭食品",
               2009: "雪糕",
               6001: "广告",
               2018: "办公图书音像",
               2019: "汽车用品",
               2021: "化工农资",
               3001: "汽车服务",
               4001: "餐饮",
               4002: "住宿",
               5002: "地磅",
               2016: "药品/计生/保健",
               2017: "通讯/数码/电脑",
               2020: "润滑油",
               2022: "其他",
               5001: "收费服务",
               2023: "积分兑换商品"}
    try:
        good_id = int(good_id)
    except Exception as e:
        logging.exception('ERROR in convert good id {0}'.format(e))
        return '', ''
    good_str = mapping.get(good_id, '其他')
    return good_str, good_str


def details_handle(details):
    detail_list = unicode(details).split(';')
    details = []
    for detail in detail_list:
        if not detail:
            continue
        detail_data = detail.split(',')
        if len(detail_data) == 0:
            continue
        if detail_data[0]:
            goods_detail, goods_cls = convert_goods(detail_data[0])
            try:
                total = detail_data[3]
            except Exception as e:
                logging.exception('ERROR in get good money reason {0}'.format(e))
                total = 0
            details.append((goods_cls, goods_detail, total))
        else:
            if len(detail_data) < 2:
                continue
            try:
                total = detail_data[3]
            except Exception as e:
                logging.exception('ERROR in get oil money reason {0}'.format(e))
                total = 0
            oil_detail, oil_cls = convert_oil_id(detail_data[1])
            details.append((oil_cls, oil_detail, total))
    return details


def get_card_record(site, start_time=None, end_time=None):
    if not start_time:
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(days=1)
    st = datetime_to_string(start_time)
    et = datetime_to_string(end_time)
    site = get_site_by_slug(site)
    ms_session = init_test()
    # ms_session = init_mysql_connect(site.bos_server)
    sql = '''select id, balance, details, nozzle, cardasn, bankcard, cardType, uniqueid, recordtime
    from tbl_epstrade
    where status in (2,3,5,23) and tradeType in (10,11,13,30,21) and recordtime BETWEEN '{0}' and '{1}'
    order by recordtime desc'''.format(st, et)
    res = ms_session.execute(sql).fetchall()
    for itm in res:
        unique_id, balance, details, pump_id, card_id, bank_card_id, card_type, eps_unique_id, original_create_time = itm
        exist = check_card_record(unique_id)
        if exist:
            break
        detail_list = details_handle(details)
        for index, dt in enumerate(detail_list):
            cls, detail, total = dt
            create_card_record(unique_id='{0}{1}'.format(unique_id, index), parent_id=unique_id, card_id=card_id,
                               bank_card_id=bank_card_id, detail=detail, pump_id=pump_id, balance=balance, total=total,
                               card_type=card_type, classification=cls, eps_unique_id=eps_unique_id, belong_id=site.id,
                               original_create_time=original_create_time)
        if card_type in (1, 2):
            abnormal_type, reason = abnormal_card_check(card_id)
            if abnormal_type:
                create_abnormal_record(abnormal_type, card_id=card_id, card_type=card_type, reason=reason,
                                       belong_id=site.id)


if __name__ == '__main__':
    get_card_record('test', datetime.datetime(2017, 8, 1), datetime.datetime(2017, 8, 2))
