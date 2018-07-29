# coding: utf-8
import copy
import logging
import datetime

import tools
from define import TOKEN_HOUSE_CORE
from zbase.base.dbpool import get_connection_exception
from zbase.web.validator import T_INT, T_STR
from zbase.utils import createid

log = logging.getLogger()


class TradeOrder(object):
    TABLE = 'trade_order'
    TABLE_ID = 'id'

    MUST_KEY = {
        'mchid': T_STR,
        'openid': T_STR,
        'consumer_name': T_STR,
        'consumer_mobile': T_STR,
        'txamt': T_INT,
        'order_name': T_STR,
        'syssn': T_STR,
        'retcd': T_STR,
        'status': T_INT,
        'cancel': T_INT,
    }

    OPTION_KEY = {
        'order_desc': T_STR,
        'origssn': T_STR,
        'note': T_STR,
        'err_desc': T_STR,
    }

    DATETIME_KEY = {
       'sysdtm': 'datetime',
       'paydtm': 'datetime',
       'ctime': 'datetime',
       'utime': 'datetime'
    }

    QUERY_KEY = {
    }

    KEYS = MUST_KEY.keys() + OPTION_KEY.keys() + DATETIME_KEY.keys()

    def __init__(self, syssn):
        self.syssn = syssn
        self.data = {}
        self.load()

    def load(self):
        where = {'syssn': self.syssn}
        keep_fields = copy.deepcopy(Order.KEYS)
        if self.TABLE_ID not in keep_fields:
            keep_fields.append(self.TABLE_ID)

        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            record = conn.select_one(table=self.TABLE, fields=keep_fields, where=where)
            self.data = record
            self.to_string(self.data)

    def update(self, values):
        log.info('func=update|syssn=%s|values=%s', self.syssn, values)
        log.info('func=update|before_update|order=%s', self.data)
        where = {'syssn': self.syssn}
        now = datetime.datetime.now()
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')
        values.update({'utime': now_str})
        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            ret = conn.update(table=self.TABLE, values=values, where=where)
            log.info('func=update|ret=%d', ret)
            return ret

    @classmethod
    def create(cls, values):
        now = datetime.datetime.now()
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')

        values['ctime'] = now_str
        values['utime'] = now_str
       
        log.info('func=create|values=%s', values)
        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            ret = conn.insert(table=cls.TABLE, values=values)
            log.info('func=create|ret=%d', ret)
            return ret

    @classmethod
    def to_string(cls, data):
        if not data:
            return
        data['id'] = str(data['id'])
        tools.trans_time(data, cls.DATETIME_KEY)