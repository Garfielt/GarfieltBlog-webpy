#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GarfieltBlog(webpy) is a light weight blog system base on web.py.It is similar 
to WordPress that provides commonly functions and featurs of a blog system.

Homepage and details: http://www.iscsky.net/

Copyright (c) 2012, Garfielt <liuwt123@gmail.com>.
License: MIT (see LICENSE.txt for details)
"""

import web
from setting import Setting
from apps.front import *
from apps.manage import *
from apps.tasks import *
from install import *

web.config.debug = Setting.is_debug

urls = (
    #Front
    '/', 'Index',
    '/page/(\d+)', 'Index',
    '/category/(.+)/page/(\d+)', 'Category',
    '/category/(.+)', 'Category',
    '/tag/(.+)/page/(\d+)', 'Tag',
    '/tag/(.+)', 'Tag',
    '/blog/(.+).html', 'Post',
    '/comment/(\d+)', 'Comment',
    '/search', 'Search',
    '/rss', 'Rss',
    '/sitemap.xml', 'Sitemap',
    '/trans/(.+)/(\d+)', 'Trans',
    '/favicon.ico', 'Favicon',
    '/valiimage', 'Valiimage',
    '/install', 'Install',
    '/install/(\d+)', 'Install',
    #Backend
    Setting.login_url, 'Login',
    '/manage/main/(\w+)', 'Manage',
    '/manage/postlist', 'ManagePostlist',
    '/manage/postlist/(\w+)/(\d+)', 'ManagePostlist',
    '/manage/post/new', 'ManagePost',
    '/manage/post/(\d+)', 'ManagePost',
    '/manage/category', 'ManageCategory',
    '/manage/category/(\w+)/(\d+)', 'ManageCategory',
    '/manage/tags', 'ManageTags',
    '/manage/tags/edit/(\d+)', 'ManageTags',
    '/manage/data', 'ManageData',
    '/manage/attachment', 'ManageAttachment',
    '/manage/comment/(\w+)/(\d+)', 'ManageComment',
    '/manage/comment', 'ManageComment',
    '/manage/links', 'ManageLinks',
    '/manage/links/(\w+)/(\d+)', 'ManageLinks',
    '/manage/setting', 'ManageSetting',
    '/manage/upload', 'ManageUpload',
    '/manage/files', 'ManageFiles',
    '/manage/user', 'ManageUser',
    '/manage/logout', 'ManageLogout',
    '/manage/result/(.+)', 'ManageResult'
)

#Init Callback interface
app = web.application(urls, globals())
if Setting.runtime == "SAE":
    import sae
    application = sae.create_wsgi_app(app.wsgifunc())
elif Setting.runtime == "BAE":
    from bae.core.wsgi import WSGIApplication
    application = WSGIApplication(app.wsgifunc())
else:
    pass


#Session Regedit
web.config.session_parameters['cookie_name'] = 'Garfitle_session'
web.config.session_parameters['cookie_domain'] = None
web.config.session_parameters['timeout'] = 86400
web.config.session_parameters['ignore_expiry'] = True
web.config.session_parameters['ignore_change_ip'] = True
web.config.session_parameters['secret_key'] = 'GarfieltSoJlRmFs6H2Ll'
web.config.session_parameters['expired_message'] = 'Session expired'

#Init Session
if mc:
    from libs.session import MemcacheStore
    store = MemcacheStore(mc)
elif Setting.runtime == "LOCAL":
    store = web.session.DiskStore('sessions')
else:
    store = web.session.DBStore(model.mdb, 'Garfielt_session')
GarfieltSession = web.session.Session(app, store, initializer={'user': ""})


#Regedit Session Hook for global Auth
def sessionHook():
    web.ctx.session = GarfieltSession

def authHook(handle):
    path = web.ctx.fullpath.lower()
    if path == Setting.login_url:
        pass
    elif path.startswith('/manage'):
        if not GarfieltSession.user:
            raise web.seeother('/')
    return handle()

app.add_processor(web.loadhook(sessionHook))
app.add_processor(authHook)

#Local run
if __name__ == "__main__":
    app.run()