#coding=utf-8

__author__ = 'dtynn'

import functools
import json
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass

    def is_user(self):
        return True

    def ajax_finish(self, msg):
        self.set_header('Content-Type', 'application/json')
        data = json.dumps(msg)
        jsonp = self.get_argument('jsonp', '')
        result = '%s(%s)' % (jsonp, data) if jsonp else data
        self.write(result)
        self.finish()
        return

    def my_redirect(self, default_url=None, arg_key='continue_url'):
        referer = self.request.headers.get('Referer', '/')
        continue_url = self.get_argument(arg_key, None)
        to_url = continue_url or default_url or referer
        self.redirect(to_url)
        return


def myauthenticated_ajax(method):
    """Decorate methods with this to require that the user be logged in."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.is_user():
            self.ajax_result(2000, 1)
            return
        return method(self, *args, **kwargs)
    return wrapper


def myauthenticated_page(method):
    """Decorate methods with this to require that the user be logged in."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.is_user():
            to_url = self.application.settings.get('login_url', '/')
            self.redirect(to_url)
            return
        return method(self, *args, **kwargs)
    return wrapper