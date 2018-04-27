# coding: utf-8
import logging
import traceback
from zbase.web import core
from house_base.response import error, RESP_CODE

log = logging.getLogger()

class BaseHandler(core.Handler):

    _get_handler_fields = []

    _post_handler_fields = []

    headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }

    def _get_handler_errfunc(self, msg):
        return error(RESP_CODE.PARAMERR, respmsg=msg)

    def _post_handler_errfunc(self, msg):
        return error(RESP_CODE.PARAMERR, respmsg=msg)

    def _get_handler(self):
        raise NotImplementedError

    def _post_handler(self):
        raise NotImplementedError

    def GET(self, *args):
        try:
            log.info('<<< %s start >>>', self.__class__.__name__)
            self.set_headers(BaseHandler.headers)
            ret = self._get_handler()
            log.info("ret: %s", ret)
            log.info('<<< %s end >>>', self.__class__.__name__)
            return self.write(ret)
        except Exception:
            log.warn(traceback.format_exc())
            return error(RESP_CODE.SERVERERR)

    def POST(self, *args):
        try:
            log.info('<<< %s start >>>', self.__class__.__name__)
            self.set_headers(BaseHandler.headers)
            ret = self._post_handler()
            log.info("ret: %s", ret)
            log.info('<<< %s end >>>', self.__class__.__name__)
            return self.write(ret)
        except Exception:
            log.warn(traceback.format_exc())
            return error(RESP_CODE.SERVERERR)