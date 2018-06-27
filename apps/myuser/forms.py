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

from apps.myuser.models import UserProfile


class LoginForm(forms.Form):
    """
    登录表单
    """
    username = forms.CharField(max_length=20, required=True)
    password = forms.CharField(min_length=6, max_length=20, required=True)


class RegisterForm(forms.Form):
    """
    注册表单
    """
    email = forms.EmailField(required=True)
    password = forms.CharField(min_length=6, max_length=20, required=True)
    captcha = CaptchaField(required=True, error_messages={'invalid': '验证码错误'})


class ForgetPwdForm(forms.Form):
    """
    忘记密码表单
    """
    email = forms.EmailField(required=True)
    captcha = CaptchaField(required=True, error_messages={'invalid': '验证码错误'})


class ResetPwdForm(forms.Form):
    """
    重置密码表单
    """
    email = forms.EmailField(required=True)
    password1 = forms.CharField(min_length=6, max_length=20, required=True)
    password2 = forms.CharField(min_length=6, max_length=20, required=True)


class UserCenUploadHeadimgForm(forms.ModelForm):
    """
    用户头像修改表单
    """
    class Meta:
        model = UserProfile
        fields = ['image']


