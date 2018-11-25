#!/usr/bin/env python
# coding:utf-8
"""
-------------------------------------------------------------
    Creator : 汪春旺
       Date : 2018-06-30
    Project : eduonline
   FileName : login_required.py
Description : 已作废。改用了内置的Mixin：LoginRequiredMixin
-------------------------------------------------------------
"""
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    """
    登录验证：
    如果验证未登录，用户自动重定向到登录页面login_url='/myuser/login/'；
    如果验证成功，用户应当自动跳反到默认存储名为"next"的查询参数中的路径。
    """

    # method_decorator类方法装饰器，传入login_required装饰器。redirect_field_name默认即为"next"
    @method_decorator(login_required(redirect_field_name='next', login_url='/myuser/login/'))
    def dispatch(self, request, *args, **kwargs):       # 必须重写分发方法dispatch，自动识别分发给get或post方法
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
