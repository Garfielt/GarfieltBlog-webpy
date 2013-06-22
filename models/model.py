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
import json
from libs.common import *
from libs.utils import *
from setting import Setting


if Setting.db_type == 'sqlite':
    mdb = sdb = web.database(dbn=Setting.db_type, db=Setting.data_dir + "/" + Setting.db_name)
elif Setting.db_type == 'mysql':
    mdb = sdb = web.database(dbn=Setting.db_type, host=Setting.db_host, port=Setting.db_port,db=Setting.db_name, user=Setting.db_user, passwd=Setting.db_passwd)
else:
    pass


class baseModel:
    def model(self):
        if Setting.db_type == 'sqlite':
            fields = sdb.query("PRAGMA table_info(" + self.tablename + ")")
            return dict_to_object(dict([[x.name, ""] for x in fields]))
        elif Setting.db_type == 'mysql':
            fields = sdb.query("show columns from " + self.tablename)
            return dict_to_object(dict([[x.Field, ""] for x in fields]))
        else:
            pass
    
    def select(self, **keywords):
        return sdb.select(self.tablename, **keywords)
    
    def insert(self, **keywords):
        return mdb.insert(self.tablename, **keywords)
    
    def delete(self, **keywords):
        return mdb.delete(self.tablename, **keywords)

    def update(self, **keywords):
        return mdb.update(self.tablename, **keywords)
    
    def query(self, sql):
        return sdb.query(sql)

class _Posts(baseModel):
    def __init__(self):
        self.tablename = Setting.db_prefix + 'posts'
    
    def get_all(self, cid = 0, plimit = 10, poffset = 1):
        if cid:
            return self.select(where='post_category=$cid',
                               order='post_id DESC',
                               limit = plimit,
                               offset = int(poffset-1) * int(plimit),
                               vars=locals())
        return self.select(order='post_id DESC',
                           limit = plimit,
                           offset = int(poffset-1) * int(plimit))
                           
    def count(self, types = '', key = None):
        if types == 'tag':
            return self.query("SELECT count(*) as total FROM " + tablename("posts") + " WHERE post_id in (select r.pid from " + tablename("relations") + " r left join " + tablename("tags") + " t on r.tid=t.tag_id where t.tag_name='%s')" % key)[0]['total']
        elif types == 'category':
            return self.query("select count(*) as total from " +\
            self.tablename + "  where post_category=%d" % key)[0]['total']
        else:
            return self.query("select count(*) as total from " + self.tablename)[0]['total']
        
    def get_by_title(self, ptitle):
        try:
            return self.select(where='post_url=$ptitle', vars=locals())[0]
        except IndexError:
            return self.model()

    def get_by_id(self, pid):
        try:
            if isinstance(pid, str):
                return self.select(where='post_id in (' + pid + ')')
            return self.select(where='post_id=$pid', vars=locals())[0]
        except IndexError:
            return self.model()
    
    def get_by_tagname(self, tagname, plimit = 10, poffset = 0):
        try:
            return self.query("SELECT * FROM " + tablename("posts") + " WHERE post_id in (select r.pid from " +\
            tablename("relations") + " r left join " + tablename("tags") +\
            " t on r.tid=t.tag_id where t.tag_name='%s') LIMIT %d OFFSET %d" % (tagname, int(plimit), int(poffset-1) * int(plimit)))
        except IndexError:
            return self.model()
    
    def get_related(self, cid=0, plimit = 5):
        what="post_id,post_title,post_url,post_date"
        if cid:
            return self.select(what=what,
                               where='post_category=$cid',
                               order="post_id DESC",
                               limit = plimit,
                               vars=locals())
        return self.select(what=what,
                           order="post_id DESC",
                           limit = plimit,
                           vars=locals())
                           
    def get_next(self, pid, direction='next'):
        if direction == 'next':
            where='post_id>$pid'
            order="post_id ASC"
        else:
            where='post_id<$pid'
            order="post_id DESC"
        try:
            return self.select(what="post_id, post_title, post_url",
                               where=where, order=order, limit = 1, vars=locals())[0]
        except IndexError:
            return None
        
    def viewcount(self, pid):
        return self.query("update " + self.tablename + " set post_view = post_view + 1 where post_id=%d" % pid)
    
    def commcount(self, pid):
        return self.query("update " + self.tablename + " set post_com_num = post_com_num + 1 where post_id=%d" % pid)
    
    def creat(self, npost):
        return self.insert(post_date = format_time(),
                           post_content = npost['pcontent'],\
                           post_title = npost['ptitle'],\
                           post_url = npost['ptstitle'],\
                           post_category = npost['pcategory'],\
                           post_type = npost['ptype'],\
                           post_tags = npost['ptags'],\
                           post_status = npost['pstatus'],\
                           post_ontop = npost['pontop'],\
                           post_com_status = int(npost['pcomment']))

    def remove(self, pid):
        return self.delete(where="post_id=$pid", vars=locals())
    
    def modify(self, pid, npost):
        return self.update(where="post_id=$pid",
                           post_content = npost['pcontent'],\
                           post_title = npost['ptitle'],\
                           post_url = npost['ptstitle'],\
                           post_category = npost['pcategory'],\
                           post_type = npost['ptype'],\
                           post_tags = npost['ptags'],\
                           post_status = npost['pstatus'],\
                           post_ontop = npost['pontop'],\
                           post_com_status = int(npost['pcomment']),\
                           vars=locals())

Posts = _Posts()


class _Category(baseModel):
    def __init__(self):
        self.tablename = Setting.db_prefix + 'categorys'
    @section_cache('Categorys_all')
    def get_all(self):
        return list(self.select(order='category_sort DESC'))
    
    def get_by_short(self, cshort):
        try:
            return self.select(where = "category_short=$cshort", vars=locals())[0]
        except IndexError:
            return self.model()

    def get_by_id(self, cid):
        try:
            return self.select(where = "category_id=$cid", vars=locals())[0]
        except IndexError:
            return self.model()
    
    def creat(self, ncat):
        return self.insert(category_name=ncat['catname'],
                           category_type=ncat['cattype'],\
                           category_sort=ncat['catsort'],\
                           category_short=ncat['catshort'],\
                           category_description=ncat['catdes'])

    def remove(self, cid):
        return self.delete(where="category_id=$cid", vars=locals())

    def modify(self, cid, ncat):
        return self.update(where="category_id=$cid",
                           category_name=ncat['catname'],\
                           category_type=ncat['cattype'],\
                           category_sort=ncat['catsort'],\
                           category_short=ncat['catshort'],\
                           category_description=ncat['catdes'],\
                           vars=locals())

Category = _Category()

class _Comments(baseModel):
    def __init__(self):
        self.tablename = Setting.db_prefix + 'comments'
        
    def get_all(self, pid = 0):
        if pid:
            return self.select(where='comments_post_id=$pid',
                              order='comments_id DESC',\
                              vars=locals())
        return self.select(order='comments_id DESC')
    
    def get_by_id(self, cid):
        try:
            return self.select(where='comments_id=$cid', vars=locals())[0]
        except IndexError:
            return self.model()
            
    def get_recent(self):
        try:
            return self.select(what="comments_id,comments_post_id,comments_author,comments_content",
                               order="comments_id DESC",
                               limit = 5,
                               vars=locals())
        except IndexError:
            return self.model()
    
    def creat(self, postid, ncom):
        return self.insert(comments_post_id=postid,
                           comments_author=ncom['author'],
                           comments_email=ncom['mail'],
                           comments_url=ncom['url'],
                           comments_ip=web.ctx.ip,
                           comments_date=format_time(),
                           comments_content=ncom['text'])
        
    def remove(self, cid):
        return self.delete(where="comments_id=$cid", vars=locals())

Comments = _Comments()

class _Links(baseModel):
    def __init__(self):
        self.tablename = Setting.db_prefix + 'links'
    
    @section_cache('Links_all')
    def get_all(self):
        return list(self.select(order='link_id DESC'))
    
    def get_by_id(self, lid):
        try:
            return self.select(where='link_id=$lid', vars=locals())[0]
        except IndexError:
            return self.model()

    def creat(self, nlink):
        return self.insert(link_url=nlink['linkurl'],
                           link_name=nlink['linkname'],\
                           link_description=nlink['linkdes'])
        
    def remove(self, lid):
        return self.delete(where="link_id=$lid", vars=locals())
    
    def modify(self, lid, nlink):
        return self.update(where="link_id=$lid",
                           link_url=nlink['linkurl'],\
                           link_name=nlink['linkname'],\
                           link_description=nlink['linkdes'],\
                           vars=locals())
 
Links = _Links()
    
class _Kvdata(baseModel):
    def __init__(self):
        self.tablename = Setting.db_prefix + 'kvdata'
        
    def get(self, kname):
        try:
            return json.loads(self.select(where='kv_name=$kname',
                                          vars=locals())[0]['kv_value'])
        except IndexError:
            return None

    def set(self, kname, ndata):
        return self.update(where="kv_name=$kname",
                           kv_value=json.dumps(ndata),\
                           vars=locals())
    
    def modify(self, kname, nkvalue):
        return self.update(where="kv_name=$kname", kv_name=nkvalue, vars=locals())

Kvdata = _Kvdata()

class _Tags(baseModel):
    def __init__(self):
        self.tablename = Setting.db_prefix + 'tags'
    
    @section_cache('Tags_all')
    def get_all(self):
        return list(self.query("select t.*,count(r.rid) as tag_num from " +\
        tablename("tags") + " t left join " + tablename("relations") +\
        " r on t.tag_id=r.tid group by t.tag_id"))
        
    def get_by_id(self, tid):
        try:
            return self.select(where='tag_id=$tid', vars=locals())[0]
        except IndexError:
            return self.model()
            
    def get_by_name(self, tname):
        try:
            return self.select(where='tag_name=$tname', vars=locals())[0]
        except IndexError:
            return self.model()
    
    @section_cache('Tag_Relations')
    def get_relations(self):
        relations = self.query("select r.pid, t.tag_name from " +\
         tablename("relations") +" r left join " + tablename("tags") +\
         " t on r.tid=t.tag_id")
        tagRelations = {}
        for r in relations:
            rkey = str(r.pid)
            if not tagRelations.has_key(rkey):
                tagRelations[rkey] = []
            tagRelations[rkey].append(r.tag_name)
        return tagRelations

    def creat(self, tagname):
        return self.insert(tag_name = tagname)
    
    def modify(self, tid, tagname):
        return self.update(where="tag_id=$tid", tag_name=tagname, vars=locals())

Tags = _Tags()

class _Relations(baseModel):
    def __init__(self):
        self.tablename = Setting.db_prefix + 'relations'
        
    def get_by_tid(self, tid):
        return self.select(where='tid=$tid', vars=locals())
    
    def get_by_pid(self, pid):
        return self.query("select t.tag_name from " + tablename("tags") + " t left join " + tablename("relations") + " r on t.tag_id=r.tid where r.pid=%d" % pid)

    def creat(self, tid, pid):
        return self.insert(tid = tid, pid = pid)
    
    def remove(self, pid):
        return self.delete(where="pid=$pid", vars=locals())
    
Relations = _Relations()

def execSql(sqlstrs):
    return list(sdb.query(sqlstrs))

    
