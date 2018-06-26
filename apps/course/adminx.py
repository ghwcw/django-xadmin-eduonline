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
from apps.course.models import Course, Section, Video, CourseResource


class CourseAdmin():
    list_display = ['id', 'name', 'desc', 'detail', 'courseorg', 'degree', 'learn_time', 'students', 'fav_nums', 'image',
                    'click_nums', 'add_time']
    list_filter = ['id', 'name', 'desc', 'detail', 'courseorg', 'degree', 'learn_time', 'students', 'fav_nums', 'image',
                   'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail']


class SectionAdmin():
    list_display = ['id', 'course', 'name', 'add_time']
    list_filter = ['id', 'course', 'name', 'add_time']
    search_fields = ['name']


class VideoAdmin():
    list_display = ['id', 'section', 'name', 'add_time']
    search_fields = ['id', 'section', 'name', 'add_time']
    list_filter = ['name']


class CourseResourceAdmin():
    list_display = ['id', 'course', 'name', 'add_time', 'download']
    search_fields = ['id', 'course', 'name', 'add_time', 'download']
    list_filter = ['id', 'course', 'name', 'add_time', 'download']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Section, SectionAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
