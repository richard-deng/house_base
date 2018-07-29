# coding: utf-8
import json
import uuid
import types
import time
import urllib
import hashlib
import requests
import logging
import datetime
import xmltodict
import traceback

import tools
import define
from tools import smart_utf8
from trade import TradeOrder
log = logging.getLogger()


class Weixin(object):

    charset = 'utf-8'

    def __init__(self, appid, app_secret, mch_id, api_key):
        self.appid = appid
        self.app_secret = app_secret
        self.mch_id = mch_id
        self.api_key = api_key

    def precreate(self, openid, body, txamt, syssn):
        data = {
            'appid': self.appid,
            'mch_id': self.mch_id,
            'nonce_str': self.gen_nonce_str(),
            'sign_type': 'MD5',
            'body': unicode(body, 'utf-8'),
            'out_trade_no': syssn,
            'total_fee': txamt,
            'spbill_create_ip': '127.0.0.1',
            'sign': '',
            'notify_url': define.NOTIFY_URL,
            'trade_type': 'JSAPI',
            'openid': openid
        }
        return data

    def gen_nonce_str(self):
        nonce_str = str(uuid.uuid4())
        nonce_str_list = nonce_str.split('-')
        nonce_str = ''.join(nonce_str_list)
        return nonce_str

    @classmethod
    def make_sign(cls, data, sign_key, not_include=('sign',)):
        keys = data.keys()
        keys.sort()
        tmp = []
        for key in keys:
            if key not in not_include and (data[key] != '' and data[key] != None):
                tmp.append("%s=%s" % (smart_utf8(key), smart_utf8(data[key])))

        tmp.append("%s=%s" % ("key", smart_utf8(sign_key)))

        tmpStr = '&'.join(tmp)
        md5 = hashlib.md5()
        md5.update(tmpStr.decode('utf-8').encode(cls.charset))
        sign = md5.hexdigest().upper()

        return sign

    def new_dict_to_xml(self, indata):
        log.debug("new_dict_to_xml=%s", indata)
        from lxml import etree
        from lxml.etree import CDATA
        root = etree.Element("xml")
        for k, v in indata.items():
            field = etree.SubElement(root, str(k))
            nv = str(v) if type(v) not in types.StringTypes else v
            log.debug("new_dict_to_xml=%s", nv)
            if k == 'detail':
                field.text = CDATA(nv)
            else:
                field.text = nv
        xmlstr = etree.tostring(root, encoding='utf-8')
        return xmlstr

    def gen_timestamp(self):
        time_str = str(int(time.time()))
        return time_str

    def send(self, method, url, req_str, key_file=None, cert_file=None, headers=None):
        log.info('fun=send|method=%s|url=%s|req_str=%s|headers=%s', method, url, req_str, headers)
        if method == 'POST':
            resp = requests.request(method, url, data=req_str, verify=False, headers=headers)
        elif method == 'GET':
            resp = requests.request(method, url, params=req_str, verify=False, headers=headers)
        else:
            raise ValueError('method=%s|not deal' % method)
        log.info('func=send|content=%s', resp.content)
        return resp.content


class GenOpenid(Weixin):

    method = 'GET'
    url = 'https://api.weixin.qq.com/sns/jscode2session'

    def build_req(self, code):
        data = {
            'appid': self.appid,
            'secret': self.app_secret,
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        log.info('class=%s|func=build_req|code=%s|data=%s', self.__class__.__name__, code, data)
        return data

    def parse_resp(self, resp_str):
        response = json.loads(resp_str)
        if 'errcode' in response:
            return None, response['errmsg']
        return response['openid'], ''
        
    def run(self, code):
        try:
            data = self.build_req(code)
            resp_str = self.send(method=self.method, url=self.url, req_str=data)
            openid, msg = self.parse_resp(resp_str)
            return openid, msg
        except Exception:
            log.warn(traceback.format_exc())
            msg = '服务异常'
            return None, msg
         

class Precreate(Weixin):

    method = 'POST'
    url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    pay_sign_temp = 'appId=%s&nonceStr=%s&package=%s&signType=%s&timeStamp=%s&key=%s'

    def build_req(self, openid, body, txamt, syssn):
        data = self.precreate(openid, body, txamt, syssn)
        sign = Weixin.make_sign(data, self.api_key)
        data['sign'] = sign
        log.info("func=build_req|with sign data=%s", data)
        xml_str = self.new_dict_to_xml(data)
        log.info("func=build_req|xml_str=%s", xml_str)
        return xml_str

    def parse_resp(self, resp_str):
        obj = xmltodict.parse(resp_str, 'utf-8')
        obj = obj['xml']
        return_code = obj['return_code']
        return_msg = obj['return_msg']
        if return_code != 'SUCCESS':
            return False, return_msg, ''

        result_code = obj['result_code']
        if result_code != 'SUCCESS':
            err_code_des = obj['err_code_des']
            return False, err_code_des, ''
        
        prepay_id = obj['prepay_id']
        return True, '', prepay_id

    def init_trade(self, syssn, openid, txamt, consumer_name, consumer_mobile, order_name, order_desc):
        sysdtm = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        trade_data = {
            'syssn': syssn,
            'openid': openid,
            'mchid': self.mch_id,
            'txamt': txamt,
            'consumer_name': consumer_name,
            'consumer_mobile': consumer_mobile,
            'order_name': order_name,
            'order_desc': order_desc,
            'sysdtm': sysdtm,
            'status': define.XC_TRADE_NOW,
            'cancel': define.XC_CANCEL_NO
        }
        ret = TradeOrder.create(trade_data)
        if ret == 1:
            return True
        return False

    def run(self, openid, txamt, consumer_name, consumer_mobile, order_name, order_desc):
        try:
            msg = ''
            log.info("func=run|openid=%s|txamt=%d", openid, txamt)
            result = {
                'timeStamp': self.gen_timestamp(),
                'nonceStr': self.gen_nonce_str(),
                'package': '',
                'signType': 'MD5',
                'paySign': '',
                'syssn': '',
            }

            syssn = tools.create_syssn()
            flag = self.init_trade(syssn, openid, txamt, consumer_name, consumer_mobile, order_name, order_desc)
            if not flag:
                msg = u'创建交易订单错误'
                return False, msg, None
            result['syssn'] = syssn

            req_str = self.build_req(openid, order_name, txamt, syssn)
            resp_str = self.send(method=self.method, url=self.url, req_str=req_str, headers=self.headers)
            wx_flag, msg, prepay_id = self.parse_resp(resp_str)
            if not wx_flag:
                return False, msg, None

            result['package'] = 'prepay_id=%s' % prepay_id
            pay_sign_str = self.pay_sign_temp % (self.appid, result['nonceStr'], result['package'], result['signType'], result['timeStamp'], self.api_key)
            log.info('pay_sign_str=%s', pay_sign_str)
            result['paySign'] = hashlib.md5(pay_sign_str).hexdigest()
            log.info('result=%s', result)
            return True, msg, result
        except Exception:
            log.warn(traceback.format_exc())
            msg = u'服务错误'
            return False, msg, None


class Query(Weixin):

    method = 'POST'
    url = 'https://api.mch.weixin.qq.com/pay/orderquery'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def build_req(self, syssn):
        log.info('func=build_req|out_trade_no=%s', syssn)
        data = {
            'appid': self.appid,
            'mch_id': self.mch_id,
            'out_trade_no': syssn,
            'nonce_str': self.gen_nonce_str(),
            'sign': '',
            'sign_type': 'MD5'
        }
        sign = self.make_sign(data, self.api_key)
        data['sign'] = sign
        log.info("func=build_req|with sign data=%s", data)
        xml_str = self.new_dict_to_xml(data)
        log.info("func=build_req|xml_str=%s", xml_str)
        return xml_str

    def parse_resp(self, resp_str):
        trade_update = {}
        obj = xmltodict.parse(resp_str, 'utf-8')
        obj = obj['xml']
        return_code = obj['return_code']
        return_msg = obj['return_msg']
        if return_code != 'SUCCESS':
            trade_update['retcd'] = define.XC_ERR_ORDER_FAIL
            trade_update['status'] = define.XC_TRADE_FAILED
            trade_update['err_desc'] = return_msg
            return trade_update

        result_code = obj['result_code']
        if result_code != 'SUCCESS':
            err_code_des = obj['err_code_des']
            trade_update['retcd'] = define.XC_ERR_ORDER_FAIL
            trade_update['status'] = define.XC_TRADE_FAILED
            trade_update['err_desc'] = err_code_des
            return trade_update

        trade_state = obj['trade_state']
        out_trade_no = obj['out_trade_no']
        trade_state_desc = obj.get('trade_state_desc')
        if trade_state != 'SUCCESS':
            if trade_state == 'NOTPAY':
                trade_update['retcd'] = define.XC_ERR_CUSTOMER_CANCEL
                trade_update['status'] = define.XC_TRADE_FAILED
                trade_update['err_desc'] = trade_state_desc if trade_state_desc else define.XC_ERR_STATE[define.XC_ERR_CUSTOMER_CANCEL]
            elif trade_state == 'CLOSED':
                trade_update['retcd'] = define.XC_ERR_ORDER_CLOSE
                trade_update['status'] = define.XC_TRADE_FAILED
                trade_update['err_desc'] = trade_state_desc if trade_state_desc else define.XC_ERR_STATE[define.XC_ERR_ORDER_CLOSE]
            elif trade_state == 'USERPAYING':
                trade_update['retcd'] = define.XC_ERR_ORDER_WAIT_PAY
                trade_update['err_desc'] = trade_state_desc if trade_state_desc else define.XC_ERR_STATE[define.XC_ERR_ORDER_WAIT_PAY]
            elif trade_state == 'PAYERROR':
                trade_update['retcd'] = define.XC_ERR_ORDER_FAIL
                trade_update['status'] = define.XC_TRADE_FAILED
                trade_update['err_desc'] = trade_state_desc if trade_state_desc else u'支付失败'
            else:
                log.warn('syssn=%s|trade_state=%s|not deal', out_trade_no, trade_state)
        else:
            trade_update['retcd'] = define.XC_OK
            trade_update['status'] = define.XC_TRADE_SUCC
            trade_update['err_desc'] = trade_state_desc

        return trade_update

    def update_trade(self, syssn, trade_update):
        to = TradeOrder(syssn=syssn)
        ret = to.update(trade_update)
        if ret == 1:
            return True
        return False

    def run(self, syssn):
        result = {}
        try:
            log.info('func=run|syssn=%s', syssn)
            record = TradeOrder(syssn=syssn)
            log.info('func=run|syssn=%s|data=%s', syssn, record.data)
            if not record.data:
                log.info('func=run|syssn=%s|not exists', syssn)
                result['retcd'] = define.XC_ERR_TRADE_NOT_EXIST
                result['status'] = ''
                result['err_desc'] = define.XC_ERR_STATE[define.XC_ERR_ORDER_NOT_EXIST]
            else:
                if record.data['retcd'] == '':
                    req_str = self.build_req(syssn)
                    resp_str = self.send(method=self.method, url=self.url, req_str=req_str, headers=self.headers)
                    trade_update = self.parse_resp(resp_str)
                    if trade_update:
                        flag = self.update_trade(syssn=syssn, trade_update=trade_update)
                        if not flag:
                            result['retcd'] = define.XC_ERR_CHANNEL_QUERY
                            result['status'] = record.data['status']
                            result['cancel'] = record.data['cancel']
                            result['err_desc'] = define.XC_ERR_STATE[define.XC_ERR_CHANNEL_QUERY]
                        else:
                            result['retcd'] = trade_update['retcd']
                            result['status'] = trade_update['status']
                            result['cancel'] = record.data['cancel']
                            result['err_desc'] = trade_update['err_desc']
                    else:
                        result['retcd'] = define.XC_ERR_CHANNEL_QUERY
                        result['status'] = record.data['status']
                        result['cancel'] = record.data['cancel']
                        result['err_desc'] = define.XC_ERR_STATE[define.XC_ERR_CHANNEL_QUERY]
                else:
                    result = {
                        'retcd': record.data['retcd'],
                        'status': record.data['status'],
                        'cancel': record.data['cancel'],
                        'err_desc': record.data['err_desc']
                    }
            log.info('func=run|normal|result=%s', result)
            return result
        except Exception:
            log.warn(traceback.format_exc())
            result['retcd'] = define.XC_ERR_CHANNEL_QUERY
            result['status'] = ''
            result['cancel'] = ''
            result['err_desc'] = define.XC_ERR_STATE[define.XC_ERR_CHANNEL_QUERY]
            log.warn('func=run|exception|result=%s', result)
            return result
