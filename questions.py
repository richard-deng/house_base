# coding: utf-8
import copy
import logging

import tools
import define
from define import TOKEN_HOUSE_CORE
from zbase.base.dbpool import get_connection_exception
from zbase.web.validator import T_INT, T_STR


log = logging.getLogger()


class Questions:

    TABLE = 'questions'
    TABLE_ID = 'id'
    MUST_KEY = {
        'parent': T_INT,
        'name': T_STR,
    }
    OPTION_KEY = {
        'category': T_INT,
        'status': T_INT,
    }
    DATETIME_KEY = {
        'ctime': 'datetime',
        'utime': 'datetime'
    }
    QUERY_KEY = {
        'name': T_STR,
    }
    KEYS = MUST_KEY.keys() + OPTION_KEY.keys() + DATETIME_KEY.keys()

    def __init__(self, box_id):
        self.id  = box_id
        self.data = {}
        self.keys = {}

    def load(self):
        where = {'id': self.id}
        keep_fields = copy.deepcopy(Questions.KEYS)
        if Questions.TABLE_ID not in keep_fields:
            keep_fields.append(Questions.TABLE_ID)

        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            record = conn.select_one(table=Questions.TABLE, fields=keep_fields, where=where)
            self.data = record
            self.to_string(self.data)

    @classmethod
    def load_root(cls):
        where = {'parent': -1, 'status': define.QUESTION_ENABLE}
        # keep_fields = copy.deepcopy(Questions.KEYS)
        keep_fields = ['id', 'name', 'category']
        if Questions.TABLE_ID not in keep_fields:
            keep_fields.append(Questions.TABLE_ID)

        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            records = conn.select(table=Questions.TABLE, fields=keep_fields, where=where)
            if records:
                for record in records:
                    cls.to_string(record)
            return records

    @classmethod
    def load_children(cls, parent):
        # 1是问题, 2是答案, 3是描述
        where = {'parent': parent, 'status': define.QUESTION_ENABLE}
        # keep_fields = copy.deepcopy(Questions.KEYS)
        keep_fields = ['id', 'name', 'category']
        if Questions.TABLE_ID not in keep_fields:
            keep_fields.append(Questions.TABLE_ID)

        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            records = conn.select(table=Questions.TABLE, fields=keep_fields, where=where)
            if records:
                for record in records:
                    cls.to_string(record)
                    record['text'] = record['name']
                    if record['category'] == 1:
                        record['icon'] = 'glyphicon glyphicon-question-sign'
                    elif record['category'] == 2:
                        record['icon'] = 'glyphicon glyphicon-info-sign'
                    else:
                        record['icon'] = 'glyphicon glyphicon-comment'
                    record['children'] = []
                    record['children'].extend(cls.load_children(record.get('id')))
            return records

    @classmethod
    def load_all(cls):
        roots = cls.load_root()
        for root in roots:
            root['children'] = []
            root['text'] = root.get('name')
            root_id = root.get('id')
            children = cls.load_children(root_id)
            root['children'] = children
            log.debug('children=%s', children)
        return roots

    @classmethod
    def load_by_parent_single(cls, parent):
        where = {'parent': parent, 'status': define.QUESTION_ENABLE}
        keep_fields = copy.deepcopy(Questions.KEYS)
        if Questions.TABLE_ID not in keep_fields:
            keep_fields.append(Questions.TABLE_ID)
        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            ret = conn.select(table=Questions.TABLE, fields=keep_fields, where=where)
            if ret:
                for data in ret:
                    cls.to_string(data)
            return ret

    @classmethod
    def to_string(self, data):
        if not data:
            return
        data['id'] = str(data['id'])
        tools.trans_time(data, Questions.DATETIME_KEY)

    @classmethod
    def create(cls, values):
        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            values.update({'status': 0})
            ret = conn.insert(table=Questions.TABLE, values=values)
            return ret

    def update(self, values):
        where = {'id': self.id}
        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            ret = conn.update(table=Questions.TABLE, values=values, where=where)
            return ret
