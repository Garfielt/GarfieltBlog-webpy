#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GarfieltBlog(webpy) is a light weight blog system base on web.py.It is similar 
to WordPress that provides commonly functions and featurs of a blog system.

Homepage and details: http://www.iscsky.net/

Copyright (c) 2012, Garfielt <liuwt123@gmail.com>.
License: MIT (see LICENSE.txt for details)
"""

__author__ = 'Garfielt <liuwt123@gmail.com>'
__version__ = '0.0.9beta'
__license__ = 'MIT'

import os
from libs.utils import dict_to_object

setting = {
    'version': __version__,
    'is_debug': True,
    'is_cache': False,
    'cache_time': 7 * 60 * 60,
    'data_dir': 'data',
    'upload_dir': 'static/uploads/',
    'login_url': '/manage/login',
    'bucket_domain': 'garfielt',
    'memcache':'',
    'db_type':'sqlite',
    'db_name':'Garfielt.db',
    'db_host': 'localhost',
    'db_port': 3306,
    'db_user': 'root',
    'db_passwd': 'root',
    "db_prefix": "Garfielt_",
    'config': {}
}

if 'SERVER_SOFTWARE' in os.environ:
    if os.environ['SERVER_SOFTWARE'] == 'direwolf/1.0':
        import sae.const
        setting["runtime"] = "SAE"
        setting['db_type'] = 'mysql'
        setting['db_host'] = sae.const.MYSQL_HOST
        setting['db_host_s'] = sae.const.MYSQL_HOST_S
        setting['db_port'] = int(sae.const.MYSQL_PORT)
        setting['db_user'] = sae.const.MYSQL_USER
        setting['db_passwd'] = sae.const.MYSQL_PASS
        setting['db_name'] = sae.const.MYSQL_DB
    elif os.environ['SERVER_SOFTWARE'] == "bae/1.0":
        from bae.core import const
        setting["runtime"] = "BAE"
        setting['db_type'] = 'mysql'
        setting['db_host'] = const.MYSQL_HOST
        setting['db_port'] = int(const.MYSQL_PORT)
        setting['db_user'] = const.MYSQL_USER
        setting['db_passwd'] = const.MYSQL_PASS
        setting['db_name'] = 'IRrmPqFOXqcxouYKtWzK'
        setting['AK'] = '03c4ec1c83e831d121df4f9786e0c6dc'
        setting['SK'] = '31285b38c6295b0846e9e212027823a6'
    else:
        setting["runtime"] = "LOCAL"

Setting = dict_to_object(setting)