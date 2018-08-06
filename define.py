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

# 用户类型
# 普通用户
HOUSE_USER_TYPE_NORMAL = 0
# 管理员
HOUSE_USER_TYPE_ADMIN = 1

HOUSE_USER_TYPE_MAP = {
    HOUSE_USER_TYPE_NORMAL: '普通用户',
    HOUSE_USER_TYPE_ADMIN: '管理员',
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

# 问答答案存储类型
ANSWER_SAVE_TYPE_TXT = 1
ANSWER_SAVE_TYPE_RICH = 2

# 文本存储类型
# 富文本
SAVE_TYPE_RICH = 1
# 文件
SAVE_TYPE_FILE = 2

SAVE_TYPE_MAP = {
    SAVE_TYPE_RICH: '富文本存储',
    SAVE_TYPE_FILE: '文件存储',
}


# 横幅
BANNER_ENABLE = 0
BANNER_DISABLE = 1

# 支付参数
NOTIFY_URL = 'http://api.xunchengfangfu.com:80/v1/api/weixin/notify'
REFUND_NOTIFY_URL = 'http://api.xunchengfangfu.com:80/v1/api/weixin/refund/notify'

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

WX_TRADE_STATE = {
    'SUCCESS': u'支付成功',
    'REFUND': u'转入退款',
    'NOTPAY': u'未支付',
    'CLOSED': u'已关闭',
    'REVOKED' : u'已撤销（刷卡支付）',
    'USERPAYING': u'用户支付中',
    'PAYERROR': u'支付失败(其他原因，如银行返回失败)'
}


XC_OK                               = "0000"
XC_ERR_REFUNDED                     = "1125"
# 原交易信息不匹配
XC_ERR_ORIG_TRADE                   = "1126"
# 数据库错误
XC_ERR_DB                           = "1127"
# 交易不存在
XC_ERR_TRADE_NOT_EXIST              = "1136"
# 订单已关闭
XC_ERR_ORDER_CLOSE                  = "1142"
# 交易不存在
XC_ERR_ORDER_NOT_EXIST              = "1143"
# 请求处理失败(协议)
XC_ERR_ORDER_FAIL                   = "1144"
# 订单状态等待支付
XC_ERR_ORDER_WAIT_PAY               = "1145"
# 订单处理业务错误
XC_ERR_ORDER_TRADE_FAIL             = "1146"
# 预授权完成金额错误
XC_ERR_PAUTHCP_AMOUNT               = "1153"
# 内部错误
XC_ERR_INTERNAL                     = "1154"
# 不允许撤销的交易
XC_ERR_REFUND_DENY                  = "1155"
# 交易结果未知，须查询
XC_ERR_CHANNEL_QUERY                = "1161"
# 订单过期
XC_ERR_ORDER_EXPIRED                = "1181"
# 消费者余额不足
XC_ERR_CUSTOMER_NOT_ENOUGH          = "2004"
# 消费者二维码过期
XC_ERR_CUSTOMER_QR_EXPIRE           = "2005"
# 消费者二维码非法
XC_ERR_CUSTOMER_QR_INVALID          = "2006"
# 消费者关闭了这次交易
XC_ERR_CUSTOMER_CANCEL              = "2007"
# 传递给通道的参数错误
XC_ERR_TO_CHNL_PARAM                = "2008"
# 连接通道失败
XC_ERR_TO_CHNL_CONNECT              = "2009"
# 和通道交互的未知错误
XC_ERR_TO_CHNL_UNKOWN               = "2010"
# 交易流水号重复
XC_ERR_SYSSN_USED                   = "2011"
# 用户的通道证书配置错误
XC_ERR_USER_CERT                    = "2012"
# 请求通道超时
XC_ERR_TO_CHNL_TIMEOUT              = "2013"
# 通道处理中
XC_ERR_CHNL_PROCESSING              = "2999"

XC_ERR_STATE = {
    XC_OK: u'正常',
    XC_ERR_REFUNDED: u'已退货',
    XC_ERR_ORIG_TRADE: u'原交易信息不匹配',
    XC_ERR_DB: u'数据库错误',
    XC_ERR_TRADE_NOT_EXIST     : u'交易不存在',
    XC_ERR_ORDER_FAIL          : u'协议处理失败',
    XC_ERR_ORDER_WAIT_PAY: u'订单已创建等待支付完成',
    XC_ERR_ORDER_TRADE_FAIL: u'订单业务处理失败',
    XC_ERR_PAUTHCP_AMOUNT: u'预授权完成金额错误',
    XC_ERR_INTERNAL: u'内部错误',
    XC_ERR_REFUND_DENY: u'不允许撤销的交易',
    XC_ERR_CHANNEL_QUERY: u'交易结果未知，须查询',
    XC_ERR_ORDER_EXPIRED: u'订单过期',
    XC_ERR_CUSTOMER_NOT_ENOUGH: u'消费者余额不足',
    XC_ERR_CUSTOMER_QR_EXPIRE: u'消费者二维码过期',
    XC_ERR_CUSTOMER_QR_INVALID: u'消费者二维码非法',
    XC_ERR_CUSTOMER_CANCEL: u'消费者关闭了这次交易',
    XC_ERR_TO_CHNL_PARAM: u'传递给通道的参数错误',
    XC_ERR_TO_CHNL_CONNECT: u'连接通道失败',
    XC_ERR_TO_CHNL_UNKOWN: u'和通道交互的未知错误',
    XC_ERR_SYSSN_USED: u'交易流水号重复',
    XC_ERR_USER_CERT: u'用户的通道证书配置错误',
    XC_ERR_TO_CHNL_TIMEOUT: u'请求通道超时',
    XC_ERR_CHNL_PROCESSING: u'通道处理中',
}
