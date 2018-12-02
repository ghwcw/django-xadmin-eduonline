#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------------------
    Creator : 汪春旺
       Date : 2018-11-20
    Project : eduonline
   FileName : mydemo.py
Description : 
-------------------------------------------------------------
"""

import os
import django
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils.translation import gettext

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduonline.settings')
django.setup()

# def my_view():
#     output = gettext("Welcome to my site.")
#     return HttpResponse(output)
#
#
# print(my_view().getvalue())

subject = 'Django测试'
message = '这是测试邮件，请忽略'
html_message = '<h2 style="color:red;">这是测试邮件，请忽略</h2>'
res = send_mail(subject=subject, message=message, from_email='Django管理员<wangchunwang@dhcc.com.cn>',
                recipient_list=['wcwnina@foxmail.com'],
                html_message=html_message)

if res:
    print('发送成功')
else:
    print('发送失败')
