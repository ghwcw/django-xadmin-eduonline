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
from apps.operation.models import UserAsk, CourseComment, UserFavorite, UserMessage, UserCourse


class UserAskAdmin():
    list_display = ['id', 'name', 'mobile', 'course_name', 'add_time']
    list_filter = ['id', 'name', 'mobile', 'course_name', 'add_time']
    search_fields = ['id', 'name', 'mobile', 'course_name', 'add_time']


class CourseCommentAdmin():
    list_display = ['id', 'user', 'course', 'comment', 'add_time']
    list_filter = ['id', 'user', 'course', 'comment', 'add_time']
    search_fields = ['id', 'user', 'course', 'comment', 'add_time']


class UserFavoriteAdmin():
    list_display = ['id', 'user', 'fav_type', 'fav_id', 'add_time']
    list_filter = ['id', 'user', 'fav_type', 'fav_id', 'add_time']
    search_fields = ['id', 'user', 'fav_type', 'fav_id', 'add_time']


class UserMessageAdmin():
    list_display = ['id', 'user', 'message', 'is_read', 'add_time']
    list_filter = ['id', 'user', 'message', 'is_read', 'add_time']
    search_fields = ['id', 'user', 'message', 'is_read', 'add_time']


class UserCourseAdmin():
    list_display = ['id', 'user', 'course', 'add_time']
    list_filter = ['id', 'user', 'course', 'add_time']
    search_fields = ['id', 'user', 'course', 'add_time']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComment, CourseCommentAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
