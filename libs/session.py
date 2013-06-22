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
import time
from web.session import Store


class MemcacheStore(Store):
    def __init__(self, mc):
        self.memcache = mc
        
    def __contains__(self, key):
        data = self.memcache.get(key)
        return bool(data)
  
    def __getitem__(self, key):
        now = time.time()
        value = self.memcache.get(key)
        if not value:
            raise KeyError
        else: 
            value['attime'] = now
            self.memcache.replace(key,value)
            return value
  
    def __setitem__(self, key, value):
        now = time.time()
        value['attime'] = now
        s = self.memcache.get(key)
        if s:
            self.memcache.replace(key,value)
        else:
		self.memcache.add(key, value, web.config.session_parameters['timeout'])
                  
    def __delitem__(self, key):
        self.memcache.delete(key)
  
    def cleanup(self, timeout):
        #timeout = timeout / (24.0 * 60 * 60)
        #last_allowed_time = time.time() - timeout 
        #self.collection.remove({'attime' : { '$lt' : last_allowed_time}}) 
        #automatic cleanup the session
        #self.memcache.flush_all()
        pass