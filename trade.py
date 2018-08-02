# coding: utf-8
import copy
import logging
import datetime
import traceback

import tools
import define
from define import TOKEN_HOUSE_CORE
from zbase.base.dbpool import get_connection_exception
from zbase.web.validator import T_INT, T_STR

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
        'openid': T_STR,
        'sysdtm': T_STR,
        'consumer_name': T_STR,
        'consumer_mobile': T_STR
    }

    KEYS = MUST_KEY.keys() + OPTION_KEY.keys() + DATETIME_KEY.keys()

    def __init__(self, syssn):
        self.syssn = syssn
        self.data = {}
        self.load()

    def load(self):
        where = {'syssn': self.syssn}
        keep_fields = copy.deepcopy(self.KEYS)
        if self.TABLE_ID not in keep_fields:
            keep_fields.append(self.TABLE_ID)

        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            record = conn.select_one(table=self.TABLE, fields=keep_fields, where=where)
            # tools.trans_time(record, self.DATETIME_KEY)
            tools.trans_amt(record)
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

    @classmethod
    def load_by_openid(cls, openid):
        where = {'openid': openid}
        keep_fields =[
            'syssn', 'consumer_name', 'consumer_mobile',
            'order_name', 'order_desc', 'openid', 'txamt',
            'retcd', 'status', 'cancel', 'origssn',
            'sysdtm',
        ]
        other = ' order by ctime desc '
        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            records = conn.select(table=cls.TABLE, fields=keep_fields, where=where, other=other)
            log.info('openid=%s|records=%s', openid, records)
            if records:
                for record in records:
                    # cls.to_string(record)
                    if record['retcd'] == '':
                        record['retcd'] = define.XC_ERR_ORDER_WAIT_PAY
                    tools.trans_time(record, cls.DATETIME_KEY)
                    tools.trans_amt(record)
            return records

    def update_refund_trade(self, trade_update, orig_trade_update):
        log.info('func=update_refund_trade|trade_update=%s|orig_trade_update=%s', trade_update, orig_trade_update)
        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            flag = True
            try:
                now_str = datetime.datetime.now().strftim('%Y-%m-%d %H:%M:%S')
                trade_update['utime'] = now_str
                orig_trade_update['utime'] = now_str
                origssn = self.data['origssn']
                orig_where = {'syssn': origssn, 'retcd': define.XC_OK, 'status': define.XC_TRADE_SUCC}
                conn.start()
                orig_ret = conn.update(table=self.TABLE, where=orig_where, values=orig_trade_update)
                if orig_ret != 1:
                    conn.rollback()
                    flag = False
                else:
                    ret = conn.update(table=self.TABLE, where={'syssn': self.syssn}, values=trade_update)
                    if ret != 1:
                        conn.rollback()
                        flag = False
                    else:
                        conn.commit()
                log.info('func=update_refund_trade|normal|flag=%s', flag)
                return flag
            except Exception:
                conn.rollback()
                flag = False
                log.warn(traceback.format_exc())
                log.info('func=update_refund_trade|except|flag=%s', flag)
                return flag

    @classmethod
    def page(cls, **kwargs):
        need_query = cls.QUERY_KEY.keys()
        where = {}

        other = kwargs.get('other', ' order by sysdtm desc ')
        page = kwargs.get('page', 1)
        page_size = kwargs.get('maxnum', 10)

        syssn = kwargs.get('syssn')
        start_time = kwargs.get('start_time')
        end_time = kwargs.get('end_time')

        log.debug('TRADE_ORDER_KEY=%s', cls.KEYS)
        keep_fields = copy.deepcopy(cls.KEYS)
        if cls.TABLE_ID not in keep_fields:
            keep_fields.append(cls.TABLE_ID)
        log.debug('keep_fields=%s', keep_fields)

        if syssn:
            where['syssn'] = syssn
            with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
                record = conn.select_one(table=cls.TABLE, fields=keep_fields, where=where)
                if record:
                    return [record], 1
                else:
                    return [], 0
        else:
            for k, v in kwargs.iteritems():
                if k in need_query and kwargs.get(k):
                    where[k] = kwargs.get(k)

            if start_time and end_time:
                where.update({'sysdtm': ('between', (str(start_time), str(end_time)))})

            with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
                sql = conn.select_sql(table=cls.TABLE, where=where, fields=keep_fields, other=other)
                pager = conn.select_page(sql, pagecur=page, pagesize=page_size)
                pager.split()
                return pager.pagedata.data, pager.count
