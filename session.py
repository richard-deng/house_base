#coding: utf-8
import uuid
import redis
import json
import logging
import traceback

from zbase.base import dbpool
from house_base import define
from house_base.response import (
    error,
    RESP_CODE,
)

log = logging.getLogger()


class Session:
    def __init__(self, redis_pool, c_conf, sk=None):
        self.sk = sk
        self.redis_pool = redis_pool
        self.c_conf = c_conf

    def gen_skey(self):
        self.sk = str(uuid.uuid4())

    def set_session(self, value):
        svalue = {}
        svalue["userid"] = value["userid"]
        client = redis.StrictRedis(connection_pool=self.redis_pool)
        client.set(self.sk, json.dumps(svalue))
        client.expire(self.sk, self.c_conf["expires"])

    def get_session(self):
        client = redis.StrictRedis(connection_pool=self.redis_pool)
        v = client.get(self.sk)
        if not v:
            return None
        return json.loads(v)

    def expire_session(self):
        client = redis.StrictRedis(connection_pool=self.redis_pool)
        client.expire(self.sk, self.c_conf["expires"])

    def rm_session(self):
        client = redis.StrictRedis(connection_pool=self.redis_pool)
        client.delete(self.sk)


class KickSession:
    def __init__(self, redis_pool, userid):
        self.redis_pool = redis_pool
        self.userid = userid

    def kick(self):
        client = redis.StrictRedis(connection_pool=self.redis_pool)
        while True:
            ret = client.lpop(self.userid)
            if not ret:
                break
            client.delete(ret)


class SUser:
    def __init__(self, userid, session):
        #session 检查， SESSION中的USERID和传上来的USERID是否一致
        self.sauth = False
        self.userid = int(userid)
        self.udata = None
        self.se = session

    #检查SESSION对应的USERID是否有权限获取用户数据
    def check_permission(self):
        #是否能获取SESSION
        v = self.se.get_session()
        if not v:
            return False

        log.debug("get session: %s", v)
        log.debug("cuserid: %d", self.userid)
        log.debug("suserid: %d", v["userid"])

        log.debug("self.userd: %d s_userid: %d", self.userid, v.get("userid"))
        if self.userid != v.get("userid"):
            log.debug("func=check_permission|userid not equal")
            return False

        self.load_user()
        if self.udata["state"] != define.HOUSE_USER_STATE_OK:
            log.debug("func=check_permission|user state error")
            self.se.rm_session()
            return False

        log.debug("session check ok")
        self.sauth = True
        return True

    def load_user(self):
        with dbpool.get_connection_exception(define.TOKEN_HOUSE_CORE) as conn:
            where = {'id': self.userid}
            self.udata = conn.select_one(table='auth_user', where=where)

def house_check_session(redis_pool, cookie_conf):
    def f(func):
        def _(self, *args, **kwargs):
            try:
                sk = self.get_cookie("sessionid")
                log.debug("sk: %s", sk)
                self.session = Session(redis_pool, cookie_conf, sk)

                try:
                    userid = self.req.input().pop('se_userid', None)
                    if userid:
                        userid = int(userid)
                    else:
                        log.warn('no se_userid or value is invalid')
                        return error(RESP_CODE.PARAMERR)
                    self.user = SUser(userid, self.session)
                    self.user.check_permission()
                    if not self.user.sauth:
                        msg = 'user is forbidden'
                        log.warn('userid=%s|err_msg=%s', self.user.userid, msg)
                        return error(RESP_CODE.LOGINERR)
                except Exception:
                    log.warn(traceback.format_exc())
                    return error(RESP_CODE.SERVERERR)

                x = func(self, *args, **kwargs)
                self.session.expire_session()
                return x
            except:
                log.warn(traceback.format_exc())
                return error(RESP_CODE.SERVERERR)
        return _
    return f


def house_set_cookie(redis_pool, cookie_conf):
    def f(func):
        def _(self, *args, **kwargs):
            try:
                x = func(self, *args, **kwargs)
                #创建SESSION
                self.session = Session(redis_pool, cookie_conf)
                self.session.gen_skey()

                v = json.loads(x)
                if v["respcd"] == RESP_CODE.OK:
                    self.session.set_session(v["data"])
                    self.set_cookie("sessionid", self.session.sk, **cookie_conf)
                return x
            except:
                log.warn(traceback.format_exc())
                return error(RESP_CODE.SERVERERR)
                #raise
        return _
    return f


def house_check_session_for_page(redis_pool, cookie_conf):
    def f(func):
        def _(self, *args, **kwargs):
            try:
                flag = True
                sk = self.get_cookie("sessionid")
                self.session = Session(redis_pool, cookie_conf, sk)
                v = self.session.get_session()
                if not v:
                    flag = False

                if not flag:
                    self.redirect('/mis/v1/page/login.html')

                ret = func(self, *args, **kwargs)
                return ret
            except:
                log.warn(traceback.format_exc())
                log.debug('raise except to redirect')
                self.redirect('/mis/v1/page/login.html')
        return _
    return f

