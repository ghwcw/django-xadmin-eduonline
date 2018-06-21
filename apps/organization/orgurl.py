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

from apps.organization.views import OrgListView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView

# app_name = 'org'

urlpatterns = [
    url(r'^orglist/$', OrgListView.as_view(), name='orglist'),
    url(r'orghome(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='orghome'),
    url(r'orgcourse(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='orgcourse'),
    url(r'orgdesc(?P<org_id>\d+)/$', OrgDescView.as_view(), name='orgdesc'),
    url(r'orgteacher(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='orgteacher'),

]

