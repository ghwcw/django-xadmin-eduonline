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

from apps.course.views import CourseCommentView, CourseAddCommentView
from apps.operation.views import UserAskView, AddFavView

urlpatterns = [
    url(r'^user-ask/$', UserAskView.as_view(), name='user_ask'),
    url(r'^add-fav/$', AddFavView.as_view(), name='add_fav'),
    url(r'^course-comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comment'),
    url(r'^course-add-comment/$', CourseAddCommentView.as_view(), name='course_add_comment'),

]
