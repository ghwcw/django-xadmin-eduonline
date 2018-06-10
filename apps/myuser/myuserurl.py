#!/usr/bin/env python
# coding:utf-8
"""
-------------------------------------------------------------
    Creator : 汪春旺
       Date : 2018-06-10
    Project : eduonline
   FileName : myuserurl.py
Description : 
-------------------------------------------------------------
"""
from django.conf.urls import url

from apps.myuser import views

urlpatterns = [
    url(r'^login/$', views.user_login, name='login'),
]
