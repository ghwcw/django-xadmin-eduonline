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
    search_fields = ['name', 'mobile', 'course_name']
    model_icon = 'fa fa-question'


class CourseCommentAdmin():
    list_display = ['id', 'user', 'course', 'comment', 'add_time']
    list_filter = ['id', 'user', 'course', 'comment', 'add_time']
    search_fields = ['comment']
    model_icon = 'fa fa-paint-brush'


class UserFavoriteAdmin():
    list_display = ['id', 'user', 'fav_type', 'fav_id', 'add_time']
    list_filter = ['id', 'user', 'fav_type', 'fav_id', 'add_time']
    model_icon = 'fa fa-star'


class UserMessageAdmin():
    list_display = ['id', 'user', 'message', 'has_read', 'add_time']
    list_filter = ['id', 'user', 'message', 'has_read', 'add_time']
    search_fields = ['message']
    model_icon = 'fa fa-commenting'
    actions = ['make_read']

    def make_read(self, request, queryset):
        if not request:
            self.message_user('未选中条目！', 'error')
        else:
            aff_rows = queryset.update(has_read=True)
            self.message_user('共%s条数据更新成功！' % aff_rows, 'success')

    make_read.short_description = '✔ 设为已读'


class UserCourseAdmin():
    list_display = ['id', 'user', 'course', 'add_time']
    list_filter = ['id', 'user', 'course', 'add_time']
    model_icon = 'fa fa-folder'


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComment, CourseCommentAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
