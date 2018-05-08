# coding:utf-8

class DATETIMEException(Exception):
    pass


#用户状态
# 2 通过审核，未设备激活
POSP_USER_STATE_VERIFIED = 2
# 3 已设备激活，未业务激活
POSP_USER_STATE_ACTIVE = 3
# 4 已业务激活，正常
POSP_USER_STATE_OK = 4

POSP_USER_STATE_MAP = {
    POSP_USER_STATE_VERIFIED: '设备未激活',
    POSP_USER_STATE_ACTIVE: '设备已激活，未激活业务',
    POSP_USER_STATE_OK: '业务已激活'
}

# DB TOKEN
TOKEN_HOUSE_CORE = 'house_core'

# 九宫格信息
BOX_ENABLE = 1
BOX_DISABLE = 0

# 盒子类型
BOX_TYPE_ORDER = 0
BOX_TYPE_TEXT = 1