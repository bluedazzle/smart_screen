# coding: utf-8
from __future__ import unicode_literals


class ChoiceBase(object):
    __choices__ = ()

    def get_choices(self):
        return self.__choices__

    @classmethod
    def get_display_name(cls, value):
        _names = dict(cls.__choices__)
        return _names.get(value) or ""

    @classmethod
    def all_elements(cls):
        _dict = dict(cls.__choices__)
        return _dict.keys()


class TaskStatus(ChoiceBase):
    error = 0
    start = 1
    running = 2
    finish = 3

    __choices__ = (
        (error, '错误'),
        (start, '开始'),
        (running, '运行中'),
        (finish, '完成'),
    )


