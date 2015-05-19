# !/usr/bin/env python
# -*- coding: utf8 -*-

import logging
from transwarp.web import get, view
from models import User, Blog, Comment
from apis import api

# @view('test_users.html')
# @get('/')
# def test_users():
#     users = User.find_all()
#     return dict(users=users)

@view('blogs.html')
@get('/')
def index():
    blogs = Blog.find_all()
    user = User.find_first('where email=?', 'Jon@example.com')
    return dict(blogs=blogs, user=user)

@api
@get('/api/users')
def api_get_users():
    users = User.find_by('order by created_at desc')

    for u in users:
        u.password = '******'
    return dict(users=users)