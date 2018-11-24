#!/usr/bin/env python
# coding:utf-8
"""
-------------------------------------------------------------
    Creator : 汪春旺
       Date : 2018-06-30
    Project : eduonline
   FileName : login_required.py
Description : 
-------------------------------------------------------------
"""
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    """
    登录验证：如果未登录，自动重定向到登录页面
    """

    @method_decorator(login_required(login_url='/myuser/login/'))  # 类方法装饰器，传入login_required装饰器
    def dispatch(self, request, *args, **kwargs):  # 必须重写分发方法dispatch，自动识别分发给get或post方法
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
