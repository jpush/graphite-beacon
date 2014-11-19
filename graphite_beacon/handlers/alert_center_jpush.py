import urllib
from tornado import gen, log, httpclient as hc

from . import AbstractHandler

LOGGER = log.gen_log

class AlertCenterJPushHandler(AbstractHandler):

    name = 'alert_center_jpush'

    defaults = {
    }

    def init_handler(self):
        assert self.options.get('jpush_alert_code'), 'jpush_alert_code is not defined.'
        self.client = hc.AsyncHTTPClient()

    @gen.coroutine
    def notify(self, level, *args, **kwargs):
        message = self.get_short(level, *args, **kwargs)
        params = "code=" + self.options.get('jpush_alert_code') + "&desc=" + urllib.urlencode(message)
        try:
            response = yield self.client.fetch('http://alert.jpushoa.com/v1/alert/?' + params, 'GET')
        except Exception as e:
            LOGGER.warn("Failed to send jpush alert center - %s" % params)

