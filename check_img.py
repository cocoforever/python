#!/usr/bin/env python
#coding:utf-8
"""
  Author:  cocoforever --<>
  Purpose: 
  Created: 2018/1/28
"""

from PIL import Image,ImageFilter
import urllib
import urllib3
import re
import json
import ssl
import os

if hasattr(ssl,'_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

User-Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
pic_url = ""

def get_img():
    resp = urllib.urlopen(pic_url)
    raw = resp.read()
    with open("./tmp.jpg",'wb') as fp:
        fp.write(raw)
        
    return Image.open("./tmp.jpg")

def get_sub_img(im,x,y):
    assert 0 <= x <= 3
    assert 0 <= y <= 2
    width = height = 68
    left = 5 + (67 + 5) * x
    top  = 41 + (67 + 5) * y