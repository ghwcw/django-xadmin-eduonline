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
import re

from django import forms

from apps.operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    """
    我要学习表单
    """

    class Meta:
        model = UserAsk
        exclude = ['add_time']

    def clean_mobile(self):
        """
        手机号验证
        :return:
        """
        mobile = self.cleaned_data['mobile']
        mobile_partt = '^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$'
        reobj = re.compile(mobile_partt)
        if reobj.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号非法')
