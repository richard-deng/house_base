#coding:utf-8
import datetime
import logging
try:
    import simplejson as json
except ImportError:
    import json

log = logging.getLogger()

class RESP_CODE:
    OK                    = "0000"
    DBERR                 = "2000"
    THIRDERR              = "2001"
    SESSIONERR            = "2002"
    DATAERR               = "2003"
    IOERR                 = "2004"
    LOGINERR              = "2100"
    PARAMERR              = "2101"
    USERERR               = "2102"
    ROLEERR               = "2103"
    PWDERR                = "2104"
    USERNOTEXISTS         = "2105"
    USERFORBIDDEN         = "2106"
    USERSTATEERR          = "2107"
    REQERR                = "2200"
    IPERR                 = "2201"
    NODATA                = "2300"
    DATAEXIST             = "2301"
    PHONENUMEXIST         = "2302"
    UNKOWNERR             = "2400"
    SERVERERR             = "2600"
    METHODERR             = "2601"
    VCODEERR              = "1000"

error_map = {
    RESP_CODE.OK                    : u"成功",
    RESP_CODE.DBERR                 : u"数据库查询错误",
    RESP_CODE.THIRDERR              : u"第三方系统错误",
    RESP_CODE.SESSIONERR            : u"用户未登录",
    RESP_CODE.DATAERR               : u"数据错误",
    RESP_CODE.IOERR                 : u"文件读写错误",
    RESP_CODE.LOGINERR              : u"用户登录失败",
    RESP_CODE.PARAMERR              : u"参数错误",
    RESP_CODE.USERERR               : u"用户不存在或未激活",
    RESP_CODE.ROLEERR               : u"用户身份错误",
    RESP_CODE.PWDERR                : u"密码错误",
    RESP_CODE.REQERR                : u"非法请求或请求次数受限",
    RESP_CODE.IPERR                 : u"IP受限",
    RESP_CODE.NODATA                : u"无数据",
    RESP_CODE.DATAEXIST             : u"数据已存在",
    RESP_CODE.UNKOWNERR             : u"未知错误",
    RESP_CODE.SERVERERR             : u"内部错误",
    RESP_CODE.METHODERR             : u"函数未实现",
    RESP_CODE.VCODEERR              : u"验证码错误",
    RESP_CODE.USERFORBIDDEN         : u"该用户禁止登录",
    RESP_CODE.USERSTATEERR          : u"用户状态错误",
}

def json_default_trans(obj):
    '''json对处理不了的格式的处理方法'''
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(obj, datetime.date):
        return obj.strftime('%Y-%m-%d')
    raise TypeError('%r is not JSON serializable' % obj)


def error(errcode, resperr='', respmsg='', data=None, debug=False, escape=True, encoder=None):
    global error_map
    if not resperr:
        resperr = respmsg if respmsg else error_map[errcode]
    if not data:
        data = {}
    ret = {"respcd": errcode, "respmsg": respmsg, "resperr": resperr, "data": data}
    if debug:
        log.debug('error:%s', ret)
    return json.dumps(ret, ensure_ascii=escape, cls=encoder, separators=(',', ':'), default = json_default_trans)

def success(data, resperr='', debug=False, escape=True, encoder=None):
    ret = {"respcd": "0000", "resperr": resperr, "respmsg": "", "data": data}
    if debug:
        log.debug('success:%s', ret)
    return json.dumps(ret, ensure_ascii=escape, cls=encoder, separators=(',', ':'), default = json_default_trans)
