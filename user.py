# coding: utf-8
import copy
import random
import string
import hashlib
import logging

import tools
from define import TOKEN_HOUSE_CORE
from zbase.base.dbpool import get_connection_exception
from zbase.web.validator import T_INT, T_STR

log = logging.getLogger()


def gen_passwd(password):
    pre = ''
    data_str = string.lowercase + string.digits
    data_list = list(data_str)
    len = 5
    for i in range(0, len):
        pre += random.choice(data_list)

    deal_passwd = hashlib.sha1(pre + password).hexdigest()
    finish_passwd = 'sha1$' + pre + '$' + deal_passwd
    return finish_passwd


def constant_time_compare(val1, val2):
    if len(val1) != len(val2):
        return False
    result = 0
    for x, y in zip(val1, val2):
        result |= ord(x) ^ ord(y)
    return result == 0


def get_hexdigest(algorithm, salt, raw_password):
    if algorithm == 'crypt':
        try:
            import crypt
        except ImportError:
            raise ValueError('"crypt" password algorithm not supported in this environment')
        return crypt.crypt(raw_password, salt)

    if algorithm == 'md5':
        return hashlib.md5(salt + raw_password).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(salt + raw_password).hexdigest()
    raise ValueError("Got unknown password algorithm type in password.")


def check_password(raw_password, enc_password):
    algo, salt, hsh = enc_password.split('$')
    return constant_time_compare(hsh, get_hexdigest(algo, salt, raw_password))


class User:

    TABLE = 'auth_user'
    TABLE_ID = 'id'
    MUST_KEY = {
        'username': T_STR,
        'merchant_code': T_STR,
        'user_type': T_INT,
        'state': T_INT,
        'email': T_STR,
        'mobile': T_STR,
        'password': T_STR,
        'admin_password': T_STR,
        'is_staff': T_INT,
        'is_active': T_INT,
        'is_superuser': T_INT,
        'last_login': T_STR,
        'date_joined': T_STR
    }
    OPTION_KEY = {
        'user_level': T_INT,
    }
    DATETIME_KEY = {
        'last_login': 'datetime',
        'date_joined': 'datetime'
    }
    KEYS = list(set(MUST_KEY.keys() + OPTION_KEY.keys() + DATETIME_KEY.keys()))


    def __init__(self, userid):
        self.userid = userid
        self.data = {}
        self.login = False
        self.keys = User.KEYS

    @classmethod
    def load_user_by_mobile(cls, mobile):
        where = {'mobile': mobile}
        keep_fields = copy.deepcopy(cls.KEYS)
        keep_fields.append(cls.TABLE_ID)
        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            record = conn.select_one(table=User.TABLE, fields=keep_fields, where=where)
            log.debug('func=load_user_by_mobile|mobile=%s|record=%s', mobile, record)
            cls.data = record
            cls.userid = record.get('id') if record else None
            return cls

    def load(self):
        where = {'id': self.userid}
        keep_fields = copy.deepcopy(self.keys)
        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            record = conn.select_one(table=User.TABLE, fields=keep_fields, where=where)
            self.data = tools.trans_time(record, User.DATETIME_KEY)