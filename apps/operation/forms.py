#!/usr/bin/env python
# coding:utf-8
"""
-------------------------------------------------------------
    Creator : 汪春旺
       Date : 2018-06-20
    Project : eduonline
   FileName : forms.py
Description : 
-------------------------------------------------------------
"""
from django import forms

from apps.operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        exclude = ['add_time']
