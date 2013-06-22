#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import web
from setting import Setting
from models import model
from libs.common import *
from libs.utils import *

render = web.template.render('template', globals={'Pformat': post_format})

class Rss():
    @section_cache('Rss')
    def GET(self):
        posts = model.Posts.get_all(None, 20)
        web.header('Content-Type', 'text/xml')
        return render.rss(Setting.config, posts)

class Sitemap():
    @section_cache('Sitemap')
    def GET(self):
        categorys = model.Category.get_all()
        posts = model.Posts.get_related(None, 1000)
        web.header('Content-Type', 'text/xml')
        return render.sitemap(Setting.config, categorys, posts)