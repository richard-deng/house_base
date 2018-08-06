# coding: utf-8
import logging
import datetime
import calendar
from define import TOKEN_HOUSE_CORE
from zbase.base.dbpool import get_connection_exception

log = logging.getLogger()


def trans_time(data, datetime_keys):
    if not data:
        return {}

    for key, data_type in datetime_keys.iteritems():
        if data.get(key):
            if data_type in ('time', 'date'):
                data[key] = str(data[key])
            elif data_type == 'datetime':
                data[key] = data.get(key).strftime('%Y-%m-%d %H:%M:%S')
            else:
                pass
    return data


def gen_trade_table_list(start_time, end_time):

    trade_table_list = []
    start_time = start_time.replace(hour=0, minute=0, second=0)
    while start_time <= end_time:
        trade_table_list.append('record_' + start_time.strftime('%Y%m'))
        mdays = calendar.monthrange(start_time.year, start_time.month)[1]
        start_time = start_time.replace(day=1) + datetime.timedelta(days=mdays)

    return trade_table_list


def trans_amt(data):
    if not data:
        return data

    txamt = data.get('txamt', 0)
    amount = txamt / 100.0
    txamt = '%.2f' % amount
    data['txamt'] = txamt
    return data


def smart_utf8(strdata):
    ''' strdata转换为utf-8编码字符串'''
    return strdata.encode('utf-8') if isinstance(strdata, unicode) else str(strdata)


def create_syssn(record_date=None):
    """
    生成交易记录流水号，规则为： 年月日+2位保留+8位自增ID。 共计18位
    """

    if record_date is None:
         record_date = datetime.date.today()

    with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
        ret  = conn.get("select uuid_short()", isdict=False)
        uuid = ret[0]
        seq = uuid % 100000000
        log.debug('uuid: %d, seq: %d', uuid, seq)

    fmt = "{year:0>4}{month:0>2}{day:0>2}{reserved:0>2}{seq:0>8}"
    syssn = fmt.format(
        year=record_date.year,
        month=record_date.month,
        day=record_date.day,
        reserved='00',
        seq=seq,
    )
    log.debug('create syssn: %s', syssn)

    return syssn
