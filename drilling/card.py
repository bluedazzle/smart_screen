# coding: utf-8
from __future__ import unicode_literals

from sqlalchemy import func

from drilling.models import session, CardRecord
from drilling.utils import get_today_st_et, get_today_night, get_week_st_et, create_abnormal_record


def abnormal_card_check(card_id):
    st, et = get_today_st_et()
    card_sql = session.query(CardRecord).filter(CardRecord.card_id == card_id)
    day_card_res = card_sql.filter(CardRecord.original_create_time.between(st, et))
    # 日异常判断:
    count = day_card_res.count()
    if count > 3:
        return '单日刷卡三次以上'
    day = day_card_res.filter(CardRecord.total >= 80000, CardRecord.classification_id == 100101)
    count = day.count()
    if count > 0:
        return '单笔汽油消费 800 元以上'
    net, nst = get_today_night()
    day_card_res = day_card_res.filter(CardRecord.original_create_time.between(st, net),
                                       CardRecord.original_create_time.between(nst, et))
    count = day_card_res.count()
    if count >= 3:
        return '单日深夜刷卡三次及以上'
    # 周异常判断:
    st, et = get_week_st_et()
    week_card_res = card_sql.filter(CardRecord.original_create_time.between(st, et))
    week = week_card_res.filter(CardRecord.total >= 200000, CardRecord.classification_id == 100101)
    count = week.count()
    if count > 0:
        return '一周内汽油消费2000元及以上'
    week = week_card_res.filter(CardRecord.total >= 1000000, CardRecord.classification_id == 100102)
    count = week.count()
    if count > 0:
        return '一周内柴油消费10000元及以上'
    mix = session.query(CardRecord.classification_id, func.count(1)).filter(
        CardRecord.classification_id.in_(100101, 100102),
        CardRecord.original_create_time.between(st, et)).group_by(
        CardRecord.classification_id).all()
    if mix[0][1] > 0 and mix[1][1] > 0:
        return '一周内汽柴油混刷'


def get_card_record():
    # todo 获取数据
    card_id = ''
    result = abnormal_card_check(card_id)
    if result:
        # 其他参数
        create_abnormal_record(card_id=card_id)


if __name__ == '__main__':
    pass
