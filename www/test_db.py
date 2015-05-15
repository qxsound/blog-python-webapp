# !/usr/bin/env python
# -*- coding:utf-8 -*-

from models import User, Blog, Comment
from transwarp import db

db.create_engine(user='root', password='root', database='awesomeblog')

u = User(name='Test', email='test@126.com', password='abcdefghijklmn', image='about:blank')
u.insert()
print 'new user id:', u.id

u1 = User.find_first('where email=?', 'test@126.com')
print 'find user\'s name:', u1.name

u1.delete()

u2 = User.find_first('where email=?', 'test@126.com')
print 'find user\'s name:', u2.name
