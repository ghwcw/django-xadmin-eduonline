#!/usr/bin/env python
# coding:utf-8
"""
-------------------------------------------------------------
    Creator : 汪春旺
       Date : 2018-06-10
    Project : eduonline
   FileName : adminx.py
Description : 
-------------------------------------------------------------
"""
import xadmin
from apps.myuser.models import EmailValiRecord, Banner


class EmailValiRecordAdmin():
    list_display = ['id', 'code', 'email', 'send_type', 'send_time']
    search_fields = ['id', 'code', 'email', 'send_type', 'send_time']
    list_filter = ['id', 'code', 'email', 'send_type', 'send_time']


class BannerAdmin():
    list_display = ['id', 'title', 'image', 'imgurl', 'index', 'add_time']
    search_fields = ['id', 'title', 'image', 'imgurl', 'index', 'add_time']
    list_filter = ['id', 'title', 'image', 'imgurl', 'index', 'add_time']


xadmin.site.register(EmailValiRecord, EmailValiRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
