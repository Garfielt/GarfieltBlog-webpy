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
from models import model
from libs.common import *

Setting.config = model.Kvdata.get("setting")

class _Render:
    def __init__(self):
        self.tplfunc = {}
        self.tpldata = {}
        self.tpldir = ''
        self.tpldata['version'] = Setting.version
        self.tplfunc['UIModule'] = self.UIModule
    
    def common_data(self):
        self.tpldata['categorys'] = model.Category.get_all()
        self.tpldata['recent_posts'] = model.Posts.get_related()
        self.tpldata['tags'] = model.Tags.get_all()
        self.tpldata['related_tags'] = model.Tags.get_relations()
        self.tpldata['links'] = model.Links.get_all()
        self.tpldata['recent_comments'] = model.Comments.get_recent()
        self.tplfunc['Post_format'] = post_format
    
    def render(self, tplname, **kwargs):
        self.tpldata['setting'] = Setting.config
        for key in kwargs:
            self.tpldata[key] = kwargs[key]
        return getattr(self.robject(), tplname)(self.tpldata)
    
    def UIModule(self, tplname):
        return self.render(tplname)
        
    def addtplfunc(self, func, quotfunc):
        self.tplfunc[func] = quotfunc
    
    def gettpldir(self):
        path = web.ctx.fullpath.lower()
        if path.startswith('/manage') or path == Setting.login_url:
            return 'manage'
        else:
            return Setting.config['template']
    
    def result(self, flag, url, msg):
        return self.render('result', flag=flag, url=url, msg=msg)
    
    def robject(self):
        return web.template.render('template/' + self.gettpldir(), globals=self.tplfunc)

Render = _Render()

__ALL__ = ['Render']