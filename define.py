# coding:utf-8

class DATETIMEException(Exception):
    pass


#用户状态
# 2 通过审核，未设备激活
HOUSE_USER_STATE_VERIFIED = 2
# 3 已设备激活，未业务激活
HOUSE_USER_STATE_ACTIVE = 3
# 4 已业务激活，正常
HOUSE_USER_STATE_OK = 4

HOUSE_USER_STATE_MAP = {
    HOUSE_USER_STATE_VERIFIED: '未激活',
    HOUSE_USER_STATE_ACTIVE: '已激活',
    HOUSE_USER_STATE_OK: '已激活'
}

# DB TOKEN
TOKEN_HOUSE_CORE = 'house_core'

# 九宫格信息
BOX_ENABLE = 1
BOX_DISABLE = 0

# 盒子类型
BOX_TYPE_ORDER = 0          # 订单
BOX_TYPE_TEXT = 1           # 文本
BOX_TYPE_INLINE_BOX = 2     # 分类

# 文本信息
TEXT_TITLE_ENABLE = 1
TEXT_TITLE_DISABLE = 0

# 问题状态描述
QUESTION_ENABLE = 0
QUESTION_DISABLE = 1

# 问答类型
QUESTION = 1
ANSWER = 2
DESCRIPTION = 3

# 问答类型描述
QUESTION_MAP = {
    QUESTION: '问题',
    ANSWER: '答案',
    DESCRIPTION: '描述',
}

# 问答状态描述
QUESTION_STATUS_ENABLE = 0
QUESTION_STATUS_DISABLE = 1
QUESTION_STATUS = {
    QUESTION_STATUS_ENABLE: '打开',
    QUESTION_STATUS_DISABLE: '关闭'
}

# 支付参数
API_KEY = 'bd0da4b891fb51e562a02fb46f729c65'
APPID = 'wxc664f270979d8d6c'
MCH_ID = '1508140221'
SECRET = 'fe4aed51980e99b55ec19774faddcd3c'
NOTIFY_URL = 'http://api.xunchengfangfu.com:80/v1/api/weixin/notify'


# ---- 交易状态 ----
# 交易中
XC_TRADE_NOW                        = 0
# 交易成功
XC_TRADE_SUCC                       = 1
# 交易失败
XC_TRADE_FAILED                     = 2
# 交易超时
XC_TRADE_TIMEOUT                    = 3

trade_state = {
    XC_TRADE_NOW: u'交易中',
    XC_TRADE_SUCC: u'交易成功',
    XC_TRADE_FAILED: u'交易失败',
    XC_TRADE_TIMEOUT: u'交易超时',
}

# ---- 取消状态 ----
XC_CANCEL_NO                        = 0
# 已冲正
XC_CANCEL_REVERSAL                  = 1
# 已撤销
XC_CANCEL_CANCELED                  = 2
# 已退货
XC_CANCEL_REFUND                    = 3
# 已完成预授权
XC_CANCEL_PAUTHCP                   = 4

cancel_state = {
    XC_CANCEL_NO: u'无',
    XC_CANCEL_REVERSAL: u'已冲正',
    XC_CANCEL_CANCELED: u'已撤销',
    XC_CANCEL_REFUND: u'已退货',
    XC_CANCEL_PAUTHCP: u'已预授权完成',
}
