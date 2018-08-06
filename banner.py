# coding: utf-8
import copy
import logging

import tools
import define
from define import TOKEN_HOUSE_CORE
from zbase.base.dbpool import get_connection_exception
from zbase.web.validator import T_INT, T_STR


log = logging.getLogger()


class Banners:

    TABLE = 'banners'
    TABLE_ID = 'id'
    MUST_KEY = {
        'title': T_STR,
    }
    OPTION_KEY = {
        'status': T_INT,
        'content': T_STR,
    }
    DATETIME_KEY = {
        'ctime': 'datetime',
        'utime': 'datetime'
    }
    QUERY_KEY = {
        'title': T_STR,
    }
    KEYS = MUST_KEY.keys() + OPTION_KEY.keys() + DATETIME_KEY.keys()

    def __init__(self, banner_id):
        self.id  = banner_id
        self.data = {}
        self.keys = {}

    def load(self):
        where = {'id': self.id}
        keep_fields = copy.deepcopy(self.KEYS)
        if self.TABLE_ID not in keep_fields:
            keep_fields.append(self.TABLE_ID)

        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            record = conn.select_one(table=self.TABLE, fields=keep_fields, where=where)
            self.data = record
            self.to_string(self.data)

    @classmethod
    def to_string(cls, data):
        if not data:
            return
        data['id'] = str(data['id'])
        tools.trans_time(data, cls.DATETIME_KEY)

    
    @classmethod
    def load_all(cls):
        where = {'status': define.BANNER_ENABLE}
        other = ' order by ctime desc '
        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            records = conn.select(table=cls.TABLE,  where=where, other=other)
            for record in records:
                cls.to_string(record)
            return records
        
