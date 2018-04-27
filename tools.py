# coding: utf-8
import datetime
import calendar
from define import BANK_CARD_MAP
from define import FOREIGN_MAP


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


def trans_bank_card_info(data):
    if 'cardtp' in data.keys() and 'foreign' in data.keys():
        data['cardtp_desc'] = BANK_CARD_MAP.get(data['cardtp'])
        data['foreign_desc'] = FOREIGN_MAP.get(str(data['foreign']))
    else:
        data['cardtp_desc'] = ''
        data['foreign_desc'] = ''

    return data

