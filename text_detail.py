# coding: utf-8
import copy
import logging
import datetime

from define import TOKEN_HOUSE_CORE
from zbase.base.dbpool import get_connection_exception
from zbase.web.validator import T_INT, T_STR
from zbase.utils import createid

log = logging.getLogger()


class TextDetail(object):
    TABLE = 'text_detail'
    TABLE_ID = 'id'
    MUST_KEY = {
        'text_id': T_INT,
    }
    OPTION_KEY = {
        'content': T_STR,
    }
    DATETIME_KEY = {
        'ctime': 'datetime',
        'utime': 'datetime'
    }
    QUERY_KEY = {
    }
    KEYS = MUST_KEY.keys() + OPTION_KEY.keys() + DATETIME_KEY.keys()

    def __init__(self, text_detail_id):
        self.id = text_detail_id
        self.data = {}
        self.keys = {}

    def load(self):
        where = {'id': self.id}
        keep_fields = copy.deepcopy(TextDetail.KEYS)
        if TextDetail.TABLE_ID not in keep_fields:
            keep_fields.append(TextDetail.TABLE_ID)

        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            record = conn.select_one(table=TextDetail.TABLE, fields=keep_fields, where=where)
            self.data = record
            self.to_string(self.data)

    @classmethod
    def load_by_text_id(cls, text_id):
        where = {'text_id': text_id}
        keep_fields = copy.deepcopy(TextDetail.KEYS)
        if TextDetail.TABLE_ID not in keep_fields:
            keep_fields.append(TextDetail.TABLE_ID)

        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            record = conn.select_one(table=TextDetail.TABLE, fields=keep_fields, where=where)
            cls.data = record
            cls.to_string(cls.data)
            return cls

    @classmethod
    def to_string(cls, data):
        if not data:
            return
        data['id'] = str(data['id'])

    def update(self, values):
        where = {'id': self.id}
        now = datetime.datetime.now()
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')
        values.update({'utime': now_str})
        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            ret = conn.update(table=TextDetail.TABLE, values=values, where=where)
            return ret

    @classmethod
    def create(cls, values):
        now = datetime.datetime.now()
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')
        values['ctime'] = now_str
        values['utime'] = now_str
        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            table_id = createid.new_id64(conn=conn)
            values['id'] = table_id
            ret = conn.insert(table=TextDetail.TABLE, values=values)
            return ret

    @classmethod
    def page(cls, **kwargs):
        need_query = cls.QUERY_KEY.keys()
        where = {}
        for k, v in kwargs.iteritems():
            if k in need_query and kwargs.get(k):
                where[k] = kwargs.get(k)
        other = kwargs.get('other', '')
        page = kwargs.get('page', 1)
        page_size = kwargs.get('maxnum', 10)
        log.debug('KEYS=%s', cls.KEYS)
        keep_fields = copy.deepcopy(cls.KEYS)
        if TextDetail.TABLE_ID not in keep_fields:
            keep_fields.append(cls.TABLE_ID)
        log.debug('keep_fields=%s', keep_fields)
        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            sql = conn.select_sql(table=TextDetail.TABLE, where=where, fields=keep_fields, other=other)
            pager = conn.select_page(sql, pagecur=page, pagesize=page_size)
            pager.split()
            return pager.pagedata.data, pager.count
