#!/usr/bin/env python
# coding:utf-8
"""
-------------------------------------------------------------
    Creator : 汪春旺
       Date : 2018-06-19
    Project : eduonline
   FileName : get_settingsvalue_tag.py
Description : 
-------------------------------------------------------------
"""
# 获取settings.py中变量的模板标签
from django import template

from eduonline import settings

register = template.Library()


@register.simple_tag
def settings_value(name):
    return getattr(settings, name, '')
