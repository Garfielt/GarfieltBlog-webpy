#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GarfieltBlog(webpy) is a light weight blog system base on web.py.It is similar 
to WordPress that provides commonly functions and featurs of a blog system.

Homepage and details: http://www.iscsky.net/

Copyright (c) 2012, Garfielt <liuwt123@gmail.com>.
License: MIT (see LICENSE.txt for details)
"""

import os
import re
from libs.utils import *
from setting import Setting

try: 
   import cPickle as pickle
except ImportError:
   import pickle

HTML_RE = re.compile(r"""<[^>]+>""", re.I|re.M|re.S)
mc = None

if Setting.runtime == "SAE":
    import pylibmc
    from sae.storage import Bucket
    bucket = Bucket(Setting.bucket_domain)
    try:
        mc = pylibmc.Client()
    except:
        error("SAE Memcache Error")
        
    def save(filename, filedata):
        bucket.put_object(filename, filedata)
        return bucket.generate_url(filename)

elif Setting.runtime == "BAE":
    try:
        from bae.api.memcache import BaeMemcache
        mc = BaeMemcache()
    except:
        error("BAE Memcache Error")
    
    from bae.core import const
    from bae.api import bcs
    from bae.api import logging
    
    BaeHost = const.BCS_ADDR
    #logging.debug(BaeHost + Setting.AK + Setting.SK)
    baebcs = bcs.BaeBCS(BaeHost, const.ACCESS_KEY, const.SECRET_KEY)
    logging.debug(baebcs.get_acl(Setting.bucket_domain, ' '))
    def save(filename, filedata):
        filename = filename.replace('/', '-')
        errcode, response = baebcs.put_object(Setting.bucket_domain, filename, filedata)
        if errcode != 0:
            raise Exception(response)
        return "http://" + BaeHost + "/" + Setting.bucket_domain + "/" + filename
else:
    try:
        if Setting.memcache:
            from libs import memcache
            mc = memcache.Client([Setting.memcache], debug=0)
    except:
        error("Memcache Error")
    def save(filename, filedata):
        f = None
        try:
            f = open(dir_file(filename), 'wb')
            f.write(filedata)
        except:
            pass
        finally:
            if f: f.close()
        return filename

try:
    mc.set('memcache', '1', 3600)
except:
    mc = None

def tablename(table):
    return Setting.db_prefix + table

def cache_file_name(cacheName):
    return Setting.data_dir + "/cache/" + cacheName + ".inc"

def set_cache(cacheName, cacheValue, ttl):
    if mc:
        mc.set(cacheName, cacheValue, ttl)
    elif Setting.runtime == "LOCAL":
        if 'Page' in cacheName:
            cacheValue = str(cacheValue)
        pickle.dump(cacheValue, open(cache_file_name(cacheName), "wb"))

def get_cache(cacheName):
    if mc:
        return mc.get(cacheName)
    elif Setting.runtime == "LOCAL":
        cacheFile = cache_file_name(cacheName)
        if is_file_exist(cacheFile):
            return pickle.load(open(cacheFile, "rb"))
    return None

def section_cache(sectionname, ttl = Setting.cache_time):
    def cache(func):
        def _cache(*args, **kwargs):
            if not Setting.is_cache: return func(*args, **kwargs)
            if len(args) > 1:
                cachename = "%s_%s" % (sectionname, args[1])
            else:
                cachename = sectionname
            body = get_cache(cachename)
            if not body:
                body = func(*args, **kwargs)
                set_cache(cachename, body, ttl)
            return body
        return _cache
    return cache

def post_format(post):
    if post.post_url == "":
        post.url = '/%s/%d.html' % ("blog", post.post_id)
    else:
        post.url = '/%s/%s.html' % ("blog", post.post_url)
    if hasattr(post, "post_tags"):
        if post.post_tags:
            post.tags = ', '.join(["<a href='/tag/%s'>%s</a>" % (tag, tag) for tag in post.post_tags.split(',')])
        else:
            post.tags = 'None'
        if '<!-- resume -->' in post.post_content:
            post.content = post.post_content.split('<!--more-->')[0]
        else:
            post.content = HTML_RE.sub('', post.post_content[:int(Setting.config['subtitle'])])

def page_navigation(baseurl, curpage, perpage, total):
    tpage = int(total)/int(perpage)
    if int(total)%int(perpage):tpage = tpage + 1
    pagenavigation = ''
    for i in range(1, (tpage+1)):
        if curpage == i:
            pagenavigation += "<li class='current'> %d </li>" % i
        else:
            pagenavigation += "<li><a href='%s/page/%d'> %d </a></li>" % (baseurl, i, i)
    return pagenavigation


