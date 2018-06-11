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
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, required=True)
    password = forms.CharField(min_length=6, required=True)
