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
BOX_TYPE_ORDER = 0
BOX_TYPE_TEXT = 1

# 文本信息
TEXT_TITLE_ENABLE = 1
TEXT_TITLE_DISABLE = 0
