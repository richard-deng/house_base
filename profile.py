# coding: utf-8
import copy
import logging

import tools
from define import TOKEN_HOUSE_CORE
from zbase.web.validator import T_INT, T_STR
from zbase.base.dbpool import get_connection_exception

log = logging.getLogger()

class Profile:

    TABLE = 'profile'
    TABLE_ID = 'id'
    MUST_KEY = {
        'user_state': T_INT,
        'banktype': T_INT,
        'allowarea': T_INT,
        'groupid': T_INT,
        'is_developer': T_INT,
        'last_admin': T_INT,
        'brchbank_code': T_STR,
        'is_salesman': T_INT,
        'swiftCode': T_STR,
        'last_modify': T_STR,
        'licenseactive_date': T_STR,
    }
    OPTION_KEY = {
        'nickname': T_STR,
        'name': T_STR,
        'idnumber': T_STR,
        'province': T_STR,
        'city': T_STR,
        'bankname': T_STR,
        'bankuser': T_STR,
        'bankaccount': T_STR,
        'mobile': T_STR,
        'email': T_STR,
    }
    DATETIME_KEY = {
        'last_modify': 'date',
        'licenseactive_date': 'date'
    }
    KEYS = list(set(MUST_KEY.keys() + OPTION_KEY.keys() + DATETIME_KEY.keys()))

    def __init__(self, userid):
        self.userid = userid
        self.data = {}
        self.keys = Profile.KEYS
        self.load()

    def load(self):
        keep_fields = copy.deepcopy(self.keys)
        keep_fields.append(Profile.TABLE_ID)
        where = {'userid': self.userid}
        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            record = conn.select_one(table=Profile.TABLE, fields=keep_fields, where=where)
            self.data = tools.trans_time(record, Profile.DATETIME_KEY)


    def update(self, values):
        func = 'update'
        where = {'userid': self.userid}
        log.debug('func=%s|userid=%s|values=%s', func, self.userid, values)
        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            ret = conn.update(table=Profile.TABLE, values=values, where=where)
            log.debug('func=%s|userid=%s|values=%s|ret=%s', func, self.userid, values, ret)
            return ret
