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
import re

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


class UpdatePwdForm(forms.Form):
    """
    个人中心-重置密码表单
    """
    password1 = forms.CharField(min_length=6, max_length=20, required=True)
    password2 = forms.CharField(min_length=6, max_length=20, required=True)


class UserCenInfoForm(forms.ModelForm):
    """
    用户个人信息修改表单
    """
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthday', 'gender', 'address', 'mobile']

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
            raise forms.ValidationError('手机号非法！')
