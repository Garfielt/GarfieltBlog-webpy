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
import random
import cStringIO

HasePIL = True
try:
    from PIL import Image
    from PIL import ImageFont
    from PIL import ImageDraw
    from PIL import ImageFilter
except:
    HasePIL = False

def validate():
    vstr = randomStr()
    if HasePIL == False:
        return vstr, ''
    vpic = validatePicGenerate(vstr)
    fbuf = cStringIO.StringIO()
    vpic.save(fbuf, 'GIF')
    del vpic
    fbuf.seek(0)
    pbbuf = fbuf.read()
    fbuf.close()
    del fbuf
    return vstr, pbbuf

def randomStr(allowed='aAbBcCdDeEFfGghHJjKkMmnNPpQqrRSstTUuVvWwXxYyZz23456789', min=4, max=4):
    ret = ''
    length_choice = range(min, max+1)
    length = random.choice(length_choice)
    for i in range(length):
        r = random.choice(allowed)
        ret += r
    return ret

def validatePicGenerate(word, psize=(120,30), font_file='', font_size=20, format='GIF', fg=-1, bg=-1):
    if fg == -1:
        fg = random.randint(0, 0xffffff)
    if bg == -1:
        bg = fg ^ 0xffffff

    if os.path.exists(font_file):
        font = ImageFont.truetype(font_file, font_size)
    else:
        font = ImageFont.load_default()
    #
    #size = font.getsize(word)
    #
    img = Image.new('RGB', psize, bg)
    draw = ImageDraw.Draw(img)
    #
    for i in range(5):
        lines = []
        for i in range(random.randint(3,5)):
            lines.append((random.randint(0, 100), random.randint(0, 100)))        
        draw.polygon(lines, outline=fg)
    #
    width = psize[0]/len(word)
    i = 0
    for w in word:
        x = (i * width) + 1
        y = random.randint(-1, 4)
        draw.text((x, y), w, font=font, fill=fg)
        i += 1
    #
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img

__ALL__ = ['validate']