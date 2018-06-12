#!/usr/bin/env python
# coding:utf-8
"""
-------------------------------------------------------------
    Creator : 汪春旺
       Date : 2018-06-11
    Project : eduonline
   FileName : forms.py
Description : 
-------------------------------------------------------------
"""
from captcha.fields import CaptchaField
from django import forms


class LoginForm(forms.Form):
    """
    登录表单
    """
    username = forms.CharField(max_length=20, required=True)
    password = forms.CharField(min_length=6, required=True)


class RegisterForm(forms.Form):
    """
    注册表单
    """
    email = forms.EmailField(required=True)
    password = forms.CharField(min_length=6, required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})
