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
from base import Render as R
from libs.common import *
from libs.utils import *
from libs.validate import validate

class Index:
    @section_cache('Page_index')
    def GET(self, page = 1):
        curpage = int(page)
        totalpost =  model.Posts.count()
        pagestr = page_navigation('', curpage, Setting.config['listnum'], totalpost)
        posts = model.Posts.get_all(None, Setting.config['listnum'], curpage)
        R.common_data()
        return R.render('index', posts = posts, pagestr = pagestr)
        
        
class Category:
    @section_cache('Page_category')
    def GET(self, kname = "", page = 1):
        if kname:
            category_shortname = check_str(kname)
            category = model.Category.get_by_short(category_shortname)
            if category.category_id:
                curpage = int(page)
                totalpost =  model.Posts.count('category', category.category_id)
                pagestr = page_navigation('/category/' + kname, curpage, Setting.config['listnum'], totalpost)
                posts = model.Posts.get_all(category.category_id, Setting.config['listnum'], curpage)
                R.common_data()
                return R.render('index', posts = posts, pagestr = pagestr)
            raise web.seeother('/')


class Tag:
    @section_cache('Page_tag')
    def GET(self, kname = "", page = 1):
        if kname:
            tagname = check_str(kname)
            curpage = int(page)
            totalpost =  model.Posts.count('tag', tagname)
            pagestr = page_navigation('/tag/' + kname, curpage, Setting.config['listnum'], totalpost)
            posts = model.Posts.get_by_tagname(tagname, Setting.config['listnum'], curpage)
            R.common_data()
            return R.render('index', posts = posts, pagestr = pagestr)


class Search:
    def POST(self, page = 1):
        spost = web.input(s = '')
        skey = spost.s
        skey = skey.encode("utf-8")
        pagestr = ''
        posts = model.execSql("select * from " + tablename("Posts") + " where post_title like '%" + skey + "%'")
        R.common_data()
        return R.render('index', posts = posts, pagestr = pagestr)


class Post:
    def GET(self, kname):
        pname = check_str(kname)
        if is_int(pname):
            post = model.Posts.get_by_id(pname)
        else:
            post = model.Posts.get_by_title(pname)
        if post.post_id:
            model.Posts.viewcount(post.post_id)
            related_posts = model.Posts.get_related(post.post_category)
            related_comments = model.Comments.get_all(post.post_id)
            post_prev = model.Posts.get_next(post.post_id, 'down')
            post_next = model.Posts.get_next(post.post_id)
            R.common_data()
            R.addtplfunc('Md5', hash_md5)
            return R.render('post', post=post, related_posts=related_posts,
                            related_comments=related_comments,
                            post_prev=post_prev, post_next=post_next)
        raise web.seeother('/')


class Comment:
    def POST(self, postid=0):
        comment = web.input(author = '', mail = '', url='', text = '')
        model.Comments.creat(postid, comment)
        model.Posts.commcount(int(postid))
        raise web.seeother('/blog/%s.html' % str(postid))


class Favicon:
    def GET(self):
        raise web.seeother('/static/favicon.ico')


class Valicode:
    def GET(self):
        web.header('Content-Type','image/gif')
        vcode, vimgbuf = validate()
        web.ctx.session.vcode = vcode.lower()
        return vimgbuf


class Trans:
    def GET(self, ptitle, randnum):
        if Setting.config["urlTrans"] == "English":
            ptitle = ptitle.strip()
            import urllib2
            import json
            try:
                requesturl = 'http://openapi.baidu.com/public/2.0/bmt/translate?client_id=I1NHcFGro7VldncGwpBhfIfn'
                requesturl += '&q=' + urllib2.quote(ptitle.encode('utf8')) + '&from=auto&to=auto'
                response = urllib2.urlopen(requesturl).read()
                resjosn = json.loads(response)
                transTitle = resjosn['trans_result'][0]['dst']
                transTitle = safe_str(transTitle)
            except :
                transTitle = Pytrans(ptitle)
        else:
            transTitle = Pytrans(ptitle)
        transTitle = transTitle.replace(" ", "_").lower()
        post = model.Posts.get_by_title(transTitle)
        if post.post_id:
            transTitle = "%s_%d" % (transTitle, int(timestamp()))
        return "{\"transTitle\":\"" + transTitle + "\"}"

        
