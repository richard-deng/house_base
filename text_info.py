# coding: utf-8
import copy
import logging
import datetime

from define import TOKEN_HOUSE_CORE, TEXT_TITLE_ENABLE
from text_detail import TextDetail
from box_list import BoxList
from zbase.base.dbpool import get_connection_exception
from zbase.web.validator import T_INT, T_STR
from zbase.utils import createid

log = logging.getLogger()


class TextInfo(object):
    TABLE = 'text_info'
    TABLE_ID = 'id'
    MUST_KEY = {
        'box_id': T_INT,
        'name': T_STR,
        'icon': T_STR,
        'save_type': T_INT,
        'priority': T_INT,
    }
    OPTION_KEY = {
        'available': T_INT,
    }
    DATETIME_KEY = {
        'ctime': 'datetime',
        'utime': 'datetime'
    }
    QUERY_KEY = {
        'name': T_STR,
    }
    KEYS = MUST_KEY.keys() + OPTION_KEY.keys() + DATETIME_KEY.keys()

    def __init__(self, text_id):
        self.id = text_id
        self.data = {}
        self.keys = {}

    def load(self):
        where = {'id': self.id}
        keep_fields = copy.deepcopy(TextInfo.KEYS)
        if TextInfo.TABLE_ID not in keep_fields:
            keep_fields.append(TextInfo.TABLE_ID)

        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            record = conn.select_one(table=TextInfo.TABLE, fields=keep_fields, where=where)
            self.data = record
            detail = TextDetail.load_by_text_id(self.id)
            self.data.update({
                'content': detail.data.get('content') if detail.data else '',
            })
            self.to_string(self.data)

    @classmethod
    def load_by_box_id(cls, box_id):
        other = ' order by priority '
        where = {'box_id': box_id, 'available': TEXT_TITLE_ENABLE}
        keep_fields = copy.deepcopy(TextInfo.KEYS)
        if TextInfo.TABLE_ID not in keep_fields:
            keep_fields.append(TextInfo.TABLE_ID)

        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            record = conn.select(table=TextInfo.TABLE, fields=keep_fields, where=where, other=other)
            cls.data = record
            if cls.data:
                for item in cls.data:
                    detail = TextDetail.load_by_text_id(item['id'])
                    item.update({
                        'content': detail.data.get('content') if detail.data else '',
                        'text_id': str(item['id']),
                    })
                    cls.to_string(item)
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
            ret = conn.update(table=TextInfo.TABLE, values=values, where=where)
            log.info('update|values=%s|where=%s|ret=%d', values, where, ret)
            return ret

    def delete(self):
        '''做真的删除操作啊'''
        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            # 先删除text_info的记录然后删除对应的text_detail的数据
            info_where = {'id': self.id}
            detail_where = {'text_id': self.id}
            log.info("<<< do reality delete text_info and detail id=%d>>>", self.id)
            info_ret = conn.delete(table=TextInfo.TABLE, where=info_where)
            log.info("<<< info_ret =%d>>>", info_ret)
            detail_ret = conn.delete(table=TextDetail.TABLE, where=detail_where)
            log.info("<<< detail_ret =%d>>>", detail_ret)
            return True

    @classmethod
    def create(cls, values):
        now = datetime.datetime.now()
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')
        values['ctime'] = now_str
        values['utime'] = now_str
        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            table_id = createid.new_id64(conn=conn)
            values['id'] = table_id
            ret = conn.insert(table=TextInfo.TABLE, values=values)
            return ret, table_id

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
        if TextInfo.TABLE_ID not in keep_fields:
            keep_fields.append(cls.TABLE_ID)
        log.debug('keep_fields=%s', keep_fields)
        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            sql = conn.select_sql(table=TextInfo.TABLE, where=where, fields=keep_fields, other=other)
            pager = conn.select_page(sql, pagecur=page, pagesize=page_size)
            pager.split()
            return pager.pagedata.data, pager.count

    @classmethod
    def page_new(cls, **kwargs):
        # where = {'text_info.available': TEXT_TITLE_ENABLE}
        where = {}
        other = kwargs.get('other', ' order by ctime desc ')
        page = kwargs.get('page', 1)
        page_size = kwargs.get('maxnum', 10)
        log.debug('KEYS=%s', cls.KEYS)
        keep_fields = copy.deepcopy(cls.KEYS)
        if TextInfo.TABLE_ID not in keep_fields:
            keep_fields.append(cls.TABLE_ID)
        log.debug('keep_fields=%s', keep_fields)
        keep_fields = [cls.TABLE + '.' + item for item in keep_fields]
        keep_fields.extend(['box_list.id as box_id', 'box_list.name as box_name'])
        log.debug('new keep_fields=%s', keep_fields)

        on = {'text_info.box_id': 'box_list.id'}

        if 'name' in kwargs and kwargs['name']:
            where['text_info.name'] = kwargs['name']

        if 'box_name' in kwargs and kwargs['box_name']:
            # where['box_list.name'] = kwargs['box_name']
            where['box_list.name'] = ('like', '%' + str(kwargs['box_name']) + '%')

        with get_connection_exception(TOKEN_HOUSE_CORE) as conn:
            sql = conn.select_join_sql(
                table1=cls.TABLE,
                table2=BoxList.TABLE,
                on=on,
                fields=keep_fields,
                where=where,
                other=other,
            )
            pager = conn.select_page(sql, pagecur=page, pagesize=page_size)
            pager.split()
            return pager.pagedata.data, pager.count
