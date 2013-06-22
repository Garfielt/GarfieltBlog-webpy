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
import web
from setting import Setting
from models import model
from base import Render as R
from libs.common import *
from libs.utils import *

class Login:
    def GET(self):
        return R.render('login')
        
    def POST(self):
        authdata = web.input(username = '', passwd = '')
        userinfo = model.Kvdata.get(authdata.user)
        if userinfo:
            if userinfo['passwd'] == hash_md5(authdata.passwd):
                web.ctx.session.user = authdata.user
                raise web.seeother('/manage/main/index')
        else:
            raise web.seeother('/')

class Manage:
    def GET(self, frame):
        frames = ['index', 'top', 'menu']
        if frame in frames:
            return web.template.frender('template/manage/' + frame + '.html')()
        if frame == 'main':
            totalpost =  model.Posts.count()
            return R.render('main', totalpost = totalpost)

class ManagePostlist:
    def GET(self, action ='view', page = 1):
        if action == 'delete':
            model.Posts.delete(pid)
        cats = model.Category.get_all()
        curpage = int(page)
        totalpost =  model.Posts.count()
        pagestr = page_navigation('/manage/post', curpage, 15, totalpost)
        categorys = {}
        for c in cats:
            categorys[c.category_id] = c.category_name
        posts = model.Posts.get_all(None, 15, curpage)
        return R.render('postlist', posts=posts, categorys=categorys,
                        totalpost=totalpost, pagestr=pagestr)


class ManagePost:
    def GET(self, pid = 0):
        if pid:
            epost = model.Posts.get_by_id(pid)
        else:
            epost = model.Posts.model()
            epost.post_title = "在这里键入标题"
        tags = model.Tags.get_all()
        categorys = model.Category.get_all()
        return R.render('post', epost=epost, categorys=categorys, tags=tags)
        
    def POST(self, pid = 0):
        post = web.input(ptitle = '', ptstitle = '', pcategory = 0,
                         pcontent = '', ptype = 0, ptags = '', pstatus = 1,
                         pontop = 0, pcomment = 1)
        tags = post['ptags']
        if tags:
            tags = tags.replace(" ", "")
            taglist = list(set(tags.split(",")))
            post['ptags'] = ','.join(taglist)
        if pid:
            model.Posts.modify(pid, post)
            model.Relations.remove(pid)
        else:
            pid = model.Posts.creat(post)
        if tags:
            otags = dict([[t.tag_name, t.tag_id] for t in model.Tags.get_all()])
            for tag in taglist:
                if tag not in otags.keys() and len(tag)>1:
                    tid = model.Tags.creat(tag)
                    model.Relations.creat(tid, pid)
                else:
                    model.Relations.creat(otags[tag], pid)
        return R.result('success', '/manage/postlist', '文章保存成功')
        

class ManageResult:
    def GET(self, redirecturl):
        return render.result(redirecturl)


class ManageCategory:
    def GET(self, action = 'view', cid = 0):
        ecategory = model.Category.get_by_id(cid)
        if action == 'delete':
            model.Category.delete(cid)
        categorys = model.Category.get_all()
        return R.render('category', ecategory = ecategory, categorys = categorys)
        
    def POST(self):
        cats = web.input(catid = 0, cattype = 0, catname = '', catshort = '', catdes = '')
        if cats.catid:
            model.Category.modify(cats.catid, cats)
        else:
            model.Category.creat(cats)
        raise web.seeother('/manage/category')


class ManageTags:
    def GET(self, tid = 0):
        tags = model.Tags.get_all()
        etag = model.Tags.get_by_id(tid)
        return R.render('tags', etag=etag, tags=tags)
        
    def POST(self):
        ntag = web.input(tagid = 0, tagname = '')
        if ntag.tagid:
            model.Tags.modify(ntag.tagid, ntag.tagname)
        else:
            model.Tags.creat(ntag.tagname)
        raise web.seeother('/manage/tags')



class ManageData:
    def GET(self, action = ''):
        return R.render('data')
        
    def POST(self):
        spost = web.input(execsql = '')
        execsql = ''
        if spost.execsql:
            execsql = spost.execsql
            results = model.execSql(execsql)
        for r in results:
            print r
            for t in r:
                print t
        return render.data(execsql, results)


class ManageAttachment:
    def GET(self):
        home = os.getcwd()
        uploadDir = os.path.join(home, "static/uploads")
        if os.path.isdir(uploadDir):
            import time
            filedata = []
            for ifile in os.listdir(uploadDir):
                ifilepath = os.path.join(uploadDir, ifile)
                filetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.stat(ifilepath).st_ctime))
                if os.path.isdir(ifilepath):
                    filedata.append({'ftype':'D', 'fname':ifile, 'fedittime':filetime})
                else:
                    filedata.append({'ftype':'f', 'fname':ifile, 'fedittime':filetime})
            print filedata
        return R.render('attachment', filedata = filedata)
        
    def POST(self):
        spost = web.input(execsql = '')
        execsql = ''
        if spost.execsql:
            execsql = spost.execsql
            results = model.execSql(execsql)
        
        return render.sql(execsql, results)


# Comments
class ManageComment:
    def GET(self, action = 'view', cid = 0):
        if action == 'delete':
            model.Comments.remove(cid)
        comments = model.Comments.get_all()
        return R.render('comment', comments=comments)


class ManageLinks:
    def GET(self, action = 'view', lid = 0):
        if action == 'delete':
            model.Links.remove(lid)
        elink = model.Links.get_by_id(lid)
        links = model.Links.get_all()
        return R.render('links', elink=elink, links=links)
        
    def POST(self):
        nlink = web.input(linkid = 0, linkname = '', linkurl = '', linkdes = '')
        if nlink.linkid:
            model.Links.modify(nlink.linkid, nlink)
        else:
            model.Links.creat(nlink)
        raise web.seeother('/manage/links')


class ManageSetting:
    def GET(self):
        esetting = dict_to_object(model.Kvdata.get("setting"))
        home = os.getcwd()
        templateDir = os.path.join(home, "template")
        if os.path.isdir(templateDir):
            themes = []
            for ifile in os.listdir(templateDir):
                if ifile != 'manage':
                    ifilepath = os.path.join(templateDir, ifile)
                    if os.path.isdir(ifilepath):
                        themes.append(ifile)
        return R.render('setting', esetting=esetting, themes=themes)
    def POST(self):
        nsetting = web.input(webtitle = 'Garfielt Blog',
                             websubtitle = 'Welcome to Mysite!',
                             webdes = 'The Garfielt Blog',
                             webkeys = 'Garfielt, Blog, Python, web.py',
                             webcdn = '',
                             timeadjust = 0,
                             listnum = 10)
        model.Kvdata.set('setting', nsetting)
        Setting.config = model.Kvdata.get("setting")
        return R.result('success', '/manage/setting', '设置修改成功')


class ManageUser:
    def GET(self):
        return R.render('user', user=web.ctx.session.user, msg='')
        
    def POST(self):
        ninfo = web.input(newname = '', oldpwd = '', newpwd = '', repwd = '')
        if ninfo.oldpwd:
            userinfo = model.Kvdata.get(web.ctx.session.user)
            if userinfo:
                if userinfo['passwd'] == hash_md5(ninfo.oldpwd):
                    if ninfo.newname:
                        model.Kvdata.modify(web.ctx.session.user, ninfo.newname)
                        web.ctx.session.user = ninfo.newname
                        return R.render('user', user=web.ctx.session.user, msg = "用户名修改成功")
                    if ninfo.newpwd and ninfo.newpwd == ninfo.repwd:
                        model.Kvdata.set(web.ctx.session.user, {'passwd': hash_md5(ninfo.newpwd)})
                        return R.render('user', user=web.ctx.session.user, msg = "密码修改成功")
        raise web.seeother('/manage/user')

class ManageFiles:
    def GET(self):
        minfo = web.input(path='')
        if minfo.path == "":
            curdir = "static/uploads/"
        else:
             curdir = minfo.path
        home = os.getcwd()
        uploadDir = os.path.join(home, curdir)
        print uploadDir
        if os.path.isdir(uploadDir):
            filedatas = []
            i = 0
            for ifile in os.listdir(uploadDir):
                ifilepath = os.path.join(uploadDir, ifile)
                filedata = {}
                if os.path.isdir(ifilepath):
                    filedata['is_dir'] = True;
                    filedata['has_file'] = len(os.listdir(ifilepath)) > 0
                    filedata['filesize'] = getdirsize(ifilepath)
                    filedata['is_photo'] = False
                    filedata['filetype'] = ''
                else:
                    Extension = os.path.splitext(ifilepath)[1][1:]
                    filedata['is_dir'] = False;
                    filedata['has_file'] = False
                    filedata['filesize'] = getfilesize(ifilepath)
                    filedata['is_photo'] = Extension in ['jpg', 'png', 'gif', 'bmp']
                    filedata['filetype'] = Extension
                filedata['filename'] = ifile
                filedata['datetime'] = format_time(os.stat(ifilepath).st_ctime)
                filedatas.append(filedata)
                i += 1
            result = {}
            result['moveup_dir_path'] = ''
            result['current_dir_path'] = curdir
            result['current_url'] = '/' + curdir
            result['total_count'] = len(filedata)
            result['file_list'] = filedatas
            return json_data(result)


class ManageUpload:      
    def POST(self):
        uploads = web.input(imgFile = {})
        if 'imgFile' in uploads:
            filepath = uploads.imgFile.filename.replace('\\','/')
            filename = filepath.split('/')[-1]
            Extension = os.path.splitext(filename)[1]
            filename = Setting.upload_dir + format_time(tformat = "%Y%m") + '/' + format_time(tformat = "%Y-%m-%d-%H-%M-%S") + Extension
            try:            
                filename = save(filename, uploads.imgFile.file.read())
            except Exception:
                print Exception
        return '{"error": 0, "url":"' + filename + '"}'


class ManageLogout:
    def GET(self):
        web.ctx.session.user = ""
        return "<script>window.parent.location='/';</script>';"
