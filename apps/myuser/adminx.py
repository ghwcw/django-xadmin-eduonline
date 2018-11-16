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
from xadmin import views


# 定制Xadmin界面
# ********************** Begin **********************
class BaseSettings():
    enable_themes = True
    use_bootswatch = True


class GlobalSettings():
    site_title = '汪春旺网络课程后台管理系统'
    site_footer = '2018-2019 汪春旺网络科技有限公司'
    menu_style = 'accordion'

# ********************** End **********************


class EmailValiRecordAdmin():
    list_display = ['id', 'code', 'email', 'send_type', 'send_time']
    list_filter = ['id', 'code', 'email', 'send_type', 'send_time']
    search_fields = ['email']
    model_icon = 'fa fa-envelope-open'


class BannerAdmin():
    list_display = ['id', 'title', 'image', 'imgurl', 'index', 'add_time']
    list_filter = ['id', 'title', 'image', 'imgurl', 'index', 'add_time']
    search_fields = ['title', 'image']
    model_icon = 'fa fa-window-maximize'


xadmin.site.register(EmailValiRecord, EmailValiRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, GlobalSettings)
