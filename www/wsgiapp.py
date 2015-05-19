# !/usr/bin/env python
# -*- coding: utf8 -*-

import logging; logging.basicConfig(level=logging.INFO)
import os
from datetime import datetime

from transwarp import db
from transwarp.web import WSGIApplication, Jinja2TemplateEngine

from config import configs

def datetime_filter(t):
    import time
    delta = int(time.time() - t)
    if delta < 60:
        return u'1分钟前'
    if delta < 3600: # an hour
        return u'%s分钟前' % (delta // 60)
    if delta < 86400: # a day
        return u'%s小时前' % (delta // 3600)
    if delta < 604800: # a week
        return u'%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' %(dt.year, dt.month, dt.day)

db.create_engine(**configs.db)

wsgi = WSGIApplication(os.path.dirname(os.path.abspath(__file__)))


template_engine = Jinja2TemplateEngine(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
template_engine.add_filter('datetime', datetime_filter)
wsgi.template_engine = template_engine

import urls
wsgi.add_interceptor(urls.user_interceptor)
wsgi.add_interceptor(urls.manage_interceptor)
wsgi.add_module(urls)

if __name__ == '__main__':
    wsgi.run(9000, host='0.0.0.0')