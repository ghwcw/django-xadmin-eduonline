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

from apps.organization.views import OrgListView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, \
    TeacherListView, TeacherDetailView

# app_name = 'org'

urlpatterns = [
    url(r'^org-list/$', OrgListView.as_view(), name='orglist'),
    url(r'org-home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='orghome'),
    url(r'org-course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='orgcourse'),
    url(r'org-desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='orgdesc'),
    url(r'org-teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='orgteacher'),

    # 授课教师
    url(r'^teacher-list/$', TeacherListView.as_view(), name='teacherlist'),
    url(r'^teacher-detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacherdetail'),

]

