# coding: utf-8
import copy
import logging
import datetime

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
        self.load()

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

    @classmethod
    def create(cls, values):
        now = datetime.datetime.now()
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')
        values['ctime'] = now_str
        values['utime'] = now_str
        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            ret = conn.insert(table=cls.TABLE, values=values)
            return ret

    @classmethod
    def load_by_title(cls, title):
        where = {'title': title}
        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            ret = conn.select_one(table=cls.TABLE, where=where)
            return ret

    def update(self, values):
        where = {'id': self.id}
        now = datetime.datetime.now()
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')
        values.update({'utime': now_str})
        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            ret = conn.update(table=self.TABLE, values=values, where=where)
            return ret


    @classmethod
    def page(cls, **kwargs):
        need_query = cls.QUERY_KEY.keys()
        where = {}
        for k, v in kwargs.iteritems():
            if k in need_query and kwargs.get(k):
                where[k] = kwargs.get(k)
        other = kwargs.get('other', ' order by ctime desc ')
        page = kwargs.get('page', 1)
        page_size = kwargs.get('maxnum', 10)
        log.debug('BOX_LIST_KEY=%s', cls.KEYS)
        keep_fields = copy.deepcopy(cls.KEYS)
        if cls.TABLE_ID not in keep_fields:
            keep_fields.append(cls.TABLE_ID)
        log.debug('keep_fields=%s', keep_fields)
        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            sql = conn.select_sql(table=cls.TABLE, where=where, fields=keep_fields, other=other)
            pager = conn.select_page(sql, pagecur=page, pagesize=page_size)
            pager.split()
            return pager.pagedata.data, pager.count
        
