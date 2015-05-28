# !/usr/bin/env python
# -*- coding: utf8 -*-
import os,re
from datetime import datetime

from fabric.api import *

env.user = 'jon'

env.sudo_user = 'root'

env.hosts = ['192.168.8.16']

db_user = 'root'
db_password = 'root'

_TAR_FILE = 'dist-awesomeblog.tar.gz'

def _current_path():
    return os.path.abspath('.')

def _now():
    return datetime.now().strftime('%y-%m-%d_%H.%M.%S')

def build():
    '''
    Build dist package.
    '''
    includes = ['static', 'templates', 'transwarp', 'favicon.ico', '*.py']
    excludes = ['test', '.*', '*.pyc', '*.pyo']
    local('rm -f dist/%s' % _TAR_FILE)
    with lcd(os.path.join(_current_path(), 'www')):
        cmd = ['tar', '--dereference', '-czvf', '../dist/%s' % _TAR_FILE]
        cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
        cmd.extend(includes)
        local(' '.join(cmd))

_REMOTE_TMP_TAR = '/tmp/%s' % _TAR_FILE
_REMOTE_BASE_DIR = '/srv/awesomeblog'

def deploy():
    newdir = 'www-%s' % _now()
    run('rm -f %s' % _REMOTE_TMP_TAR)
    put('dist/%s' % _TAR_FILE, _REMOTE_TMP_TAR)
    with cd(_REMOTE_BASE_DIR):
        sudo('mkdir %s' % newdir)
    with cd('%s/%s' % (_REMOTE_BASE_DIR, newdir)):
        sudo('tar -xzvf %s' % _REMOTE_TMP_TAR)
    with cd(_REMOTE_BASE_DIR):
        sudo('rm -f www')
        sudo('ln -s %s www' % newdir)
        sudo('chown root:root www')
        sudo('chown -R root:root %s' % newdir)
    with settings(warn_only=True):
        sudo('supervisorctl stop awesomeblog')
        sudo('supervisorctl start awesomeblog')
        sudo('/etc/init.d/nginx reload')