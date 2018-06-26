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
from apps.organization.models import CityDict, CourseOrg, Teacher


class CityDictAdmin():
    list_display = ['id', 'name', 'desc', 'add_time']
    list_filter = ['id', 'name', 'desc', 'add_time']
    search_fields = ['name', 'desc']


class CourseOrgAdmin():
    list_display = ['id', 'name', 'desc', 'click_nums', 'fav_nums', 'image', 'city', 'address', 'add_time']
    list_filter = ['id', 'name', 'desc', 'click_nums', 'fav_nums', 'image', 'city', 'address', 'add_time']
    search_fields = ['name', 'desc', 'image', 'address']


class TeacherAdmin():
    list_display = ['id', 'org', 'name', 'work_year', 'work_company', 'work_position', 'click_nums', 'fav_nums',
                    'image', 'add_time']
    list_filter = ['id', 'org', 'name', 'work_year', 'work_company', 'work_position', 'click_nums', 'fav_nums',
                   'image', 'add_time']
    search_fields = ['name', 'work_company', 'work_position', 'image']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
