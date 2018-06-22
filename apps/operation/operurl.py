#!/usr/bin/env python
# coding:utf-8
"""
-------------------------------------------------------------
    Creator : 汪春旺
       Date : 2018-06-20
    Project : eduonline
   FileName : operurl.py
Description : 
-------------------------------------------------------------
"""
from django.conf.urls import url

from apps.operation.views import UserAskView, AddFavView

urlpatterns = [
    url(r'^userask/$', UserAskView.as_view(), name='user_ask'),
    url(r'^addfav/$', AddFavView.as_view(), name='add_fav'),

]
