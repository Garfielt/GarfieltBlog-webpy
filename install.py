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
from libs.common import *

render = web.template.render('template/manage')

class Install:
    def GET(self, step = 0):
        Isql = '''CREATE TABLE ^Garfielt_categorys$ (
^category_id$  INTEGER NOT NULL autoincrement,
^category_name$  VARCHAR(40) NOT NULL,
^category_type$  TINYINT(1) NOT NULL DEFAULT 0,
^category_sort$  INTEGER NOT NULL DEFAULT 0,
^category_short$  VARCHAR(40),
^category_description$  VARCHAR(100),
PRIMARY KEY (^category_id$ ASC)
);
CREATE TABLE ^Garfielt_comments$ (
^comments_id$  INTEGER NOT NULL autoincrement,
^comments_post_id$ INTEGER NOT NULL,
^comments_author$  VARCHAR(40) NOT NULL DEFAULT '',
^comments_email$  VARCHAR(40) NOT NULL DEFAULT '',
^comments_url$  VARCHAR(100) NOT NULL DEFAULT '',
^comments_ip$  VARCHAR(20) NOT NULL DEFAULT '',
^comments_date$  DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00',
^comments_content$  TEXT NOT NULL,
PRIMARY KEY (^comments_id$ ASC)
);
CREATE TABLE ^Garfielt_kvdata$ (
^kv_id$  INTEGER NOT NULL autoincrement,
^kv_name$  VARCHAR(40) NOT NULL DEFAULT '',
^kv_value$  TEXT NOT NULL DEFAULT '',
PRIMARY KEY (^kv_id$ ASC)
);
CREATE TABLE ^Garfielt_links$ (
^link_id$  INTEGER NOT NULL autoincrement,
^link_name$  VARCHAR(255) NOT NULL,
^link_url$  VARCHAR(255) NOT NULL,
^link_description$  VARCHAR(255) DEFAULT '',
^link_visible$  TINYINT(1) NOT NULL DEFAULT 1,
PRIMARY KEY (^link_id$ ASC)
);
CREATE TABLE ^Garfielt_posts$ (
^post_id$  INTEGER NOT NULL autoincrement,
^post_category$  INTEGER NOT NULL,
^post_type$  TINYINT(1) NOT NULL DEFAULT 0,
^post_status$  TINYINT(1) DEFAULT 1,
^post_ontop$  TINYINT(1) DEFAULT 0,
^post_title$  VARCHAR(100) NOT NULL,
^post_url$  VARCHAR(60) DEFAULT '',
^post_date$  DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00',
^post_editdate$  DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00',
^post_tags$  VARCHAR(100) DEFAULT '',
^post_view$  INTEGER NOT NULL DEFAULT 0,
^post_com_num$  INTEGER NOT NULL DEFAULT 0,
^post_com_status$  TINYINT(1) NOT NULL DEFAULT 1,
^post_content$  TEXT,
PRIMARY KEY (^post_id$ ASC)
);
CREATE TABLE ^Garfielt_tags$ (
^tag_id$  INTEGER NOT NULL autoincrement,
^tag_name$  VARCHAR(20) NOT NULL,
PRIMARY KEY (^tag_id$ ASC)
);
CREATE TABLE ^Garfielt_relations$ (
^rid$ INTEGER NOT NULL autoincrement,
^tid$ INTEGER NOT NULL,
^pid$ INTEGER NOT NULL,
PRIMARY KEY (^rid$ ASC)
);
CREATE TABLE ^Garfielt_session$ (
^session_id$ char(128) UNIQUE NOT NULL,
^atime$ timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
^data$ text
);'''
        if step == 0:
            disinfo = '''
                <a href="/install/1">click to install</a>
            '''
        elif step == "1":
            if Setting.db_type == 'sqlite':
                disinfo = Isql.replace("^","[").replace("$","]")
            else:
                disinfo = Isql.replace("^","`").replace("$","`")
                disinfo = disinfo.replace("CURRENT_TIMESTAMP","timestamp")
                disinfo = disinfo.replace("autoincrement","auto_increment")
                disinfo = disinfo.replace(";","ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;")
            disinfo = disinfo.replace("\n","<br>")
            disinfo = '数据库类型：' + Setting.db_type + '<br>' + disinfo
        
        return render.install(disinfo)