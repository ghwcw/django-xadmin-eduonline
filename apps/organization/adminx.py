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
    model_icon = 'fa fa-telegram'
    date_hierarchy = 'add_time'


class CourseOrgAdmin():
    # fields = ['name', 'city', 'desc']

    def trunc_desc(self, obj):
        return '%s......' % obj.desc[:35]
    trunc_desc.short_description = '机构描述'
    trunc_desc.admin_order_field = 'trunc_desc'

    list_display = ['id', 'name', 'trunc_desc', 'click_nums', 'fav_nums', 'image', 'city', 'address', 'add_time']
    list_filter = ['id', 'name', 'desc', 'category', 'click_nums', 'fav_nums', 'image', 'city', 'address', 'add_time']
    search_fields = ['name', 'desc', 'image', 'address']
    list_display_links = ['id', 'name']
    model_icon = 'fa fa-graduation-cap'
    # readonly_fields = ['name']
    exclude = ['click_nums']
    relfield_sytle = 'fk_ajax'

    # fieldsets = [
    #     (None, {
    #         'fields': ['name', 'desc', 'city']
    #     }),
    #     ('Advanced options', {
    #         'classes': ['collapse'],
    #         'fields': ['registration_required', 'template_name'],
    #     }),
    # ]


class TeacherAdmin():
    list_display = ['id', 'org', 'name', 'work_year', 'work_company', 'work_position', 'click_nums', 'fav_nums',
                    'image', 'add_time']
    list_filter = ['id', 'org', 'name', 'work_year', 'work_company', 'work_position', 'click_nums', 'fav_nums',
                   'image', 'add_time']
    search_fields = ['name', 'work_company', 'work_position', 'image']
    model_icon = 'fa fa-handshake-o'


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
