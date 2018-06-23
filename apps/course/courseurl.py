#!/usr/bin/env python
# coding:utf-8
"""
-------------------------------------------------------------
    Creator : 汪春旺
       Date : 2018-06-22
    Project : eduonline
   FileName : courseurl.py
Description : 
-------------------------------------------------------------
"""
from django.conf.urls import url

from apps.course.views import CourseListView, CourseDetailView

urlpatterns = [
    url(r'^courselist/$', CourseListView.as_view(), name='course_list'),
    url(r'^coursedetail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),

]
