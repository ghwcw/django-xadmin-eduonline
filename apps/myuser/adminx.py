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
from apps.myuser.models import EmailValiRecord, Banner, UserProfile
from xadmin import views
from xadmin.plugins.auth import UserAdmin


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


class UserProfileAdmin(UserAdmin):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.list_display = ['id', 'username', 'nick_name', 'email', 'is_active', 'is_staff', 'date_joined']

    list_display = ['id', 'username', 'nick_name', 'email', 'is_active', 'is_staff', 'date_joined']


xadmin.site.register(EmailValiRecord, EmailValiRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(UserProfile, UserProfileAdmin)
