#!/usr/bin/env python
# coding:utf-8
"""
-------------------------------------------------------------
    Creator : 汪春旺
       Date : 2018-06-18
    Project : eduonline
   FileName : orgurl.py
Description : 
-------------------------------------------------------------
"""
from django.conf.urls import url

from apps.organization.views import OrgListView

app_name = 'org'

urlpatterns = [
    url(r'^orglist/$', OrgListView.as_view(), name='orglist'),

]

