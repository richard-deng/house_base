# coding: utf-8
import copy
import logging
import datetime
import tools
from define import TOKEN_HOUSE_CORE
from zbase.base.dbpool import get_connection_exception
from zbase.web.validator import T_FLOAT, T_STR

log = logging.getLogger()

class RateInfo(object):
    TABLE = 'rate_info'
    TABLE_ID = 'id'
    MUST_KEY = {
        'name': T_STR,
        'rate': T_FLOAT
    }
    OPTION_KEY = {}
    DATETIME_KEY = {
        'ctime': 'datetime',
        'utime': 'datetime'
    }
    QUERY_KEY = {
        'name': T_STR,
    }

    KEYS = MUST_KEY.keys() + OPTION_KEY.keys() + DATETIME_KEY.keys()

    def __init__(self, rate_id):
        self.id = rate_id
        self.data = {}
        self.keys = {}

    def load(self):
        where = {'id': self.id}
        keep_fields = copy.deepcopy(RateInfo.KEYS)
        if RateInfo.TABLE_ID not in keep_fields:
            keep_fields.append(RateInfo.TABLE_ID)
        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            record = conn.select_one(table=RateInfo.TABLE, fields=keep_fields, where=where)
            self.data = record
            self.to_string(self.data)
            tools.trans_time(self.data, RateInfo.DATETIME_KEY)

    @classmethod
    def load_all(cls):
        keep_fields = copy.deepcopy(RateInfo.KEYS)
        if RateInfo.TABLE_ID not in keep_fields:
            keep_fields.append(RateInfo.TABLE_ID)
        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            records = conn.select(table=RateInfo.TABLE, fields=keep_fields)
            if records:
                for data in records:
                    cls.to_string(data)
                    tools.trans_time(data, cls.DATETIME_KEY)
            return records


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
            ret = conn.update(table=RateInfo.TABLE, values=values, where=where)
            return ret

    @classmethod
    def create(cls, values):
        now = datetime.datetime.now()
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')
        values.update({
            'ctime': now_str,
            'utime': now_str
        })
        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            ret = conn.insert(table=RateInfo.TABLE, values=values)
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
        if RateInfo.TABLE_ID not in keep_fields:
            keep_fields.append(cls.TABLE_ID)
        log.debug('keep_fields=%s', keep_fields)

        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            sql = conn.select_sql(table=RateInfo.TABLE, where=where, fields=keep_fields, other=other)
            pager = conn.select_page(sql, pagecur=page, pagesize=page_size)
            pager.split()
            return pager.pagedata.data, pager.count
