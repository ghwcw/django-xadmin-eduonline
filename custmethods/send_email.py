#!/usr/bin/env python
# coding:utf-8
"""
-------------------------------------------------------------
    Creator : 汪春旺
       Date : 2018-06-13
    Project : eduonline
   FileName : send_email.py
Description : 
-------------------------------------------------------------
"""
# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduonline.settings')
# import django
# django.setup()

import random
from _md5 import md5
from django.core import mail

from apps.myuser.models import EmailValiRecord
from eduonline import settings


class SendEmail():
    def __init__(self, email, send_type='register'):
        self.email = email
        self.send_type = send_type

    @staticmethod
    def create_random_str(n=8):
        """
        随机取出n个字符，然后采用哈希算法生成code。
        :param n: 取出的字符个数
        :return: 返回生成的加密字符串
        """
        string = 'qwertyuiopasdfghjklzxcvbnm0123456789'
        res_str = ''
        for _ in range(n):
            res_str += string[random.randint(0, len(string) - 1)]

        md5_obj = md5(res_str.encode())
        return md5_obj.hexdigest()

    def send_acti_email(self):
        """
        发送验证邮件
        :return:
        """
        email_valid = EmailValiRecord()
        code = SendEmail.create_random_str()
        email_valid.code = code
        email_valid.email = self.email
        email_valid.send_type = self.send_type
        email_valid.save()

        if self.send_type == 'register':
            subject = '网络教育在线注册激活'
            text_content = '请确认邮件后，点击该链接进行账号激活：http://127.0.0.1:8000/activate/reg/{0}'.format(code)
            html_content = '<h2>请确认邮件后，点击下方链接进行账号激活：</h2><a href="http://127.0.0.1:8000/activate/reg/{0}">http://127.0.0.1:8000/activate/reg/{0}</a>'.format(
                code)
            # mail_status = mail.send_mail(subject=subject, message=text_content,
            #                              from_email='网络教育<{0}>'.format(settings.EMAIL_HOST_USER),
            #                              recipient_list=[self.email])
            msg = mail.EmailMultiAlternatives(subject=subject, body=text_content,
                                              from_email='网络教育<{0}>'.format(settings.EMAIL_HOST_USER), to=[self.email])
            msg.attach_alternative(content=html_content, mimetype='text/html')
            mail_status = msg.send()

            if mail_status:
                return True
            else:
                return False

        elif self.send_type == 'forget':
            subject = '网络教育在线重置密码'
            text_content = '请确认邮件后，点击该链接进行重置密码：http://127.0.0.1:8000/activate/resetpwd/{0}'.format(code)
            html_content = '<h2>请确认邮件后，点击下方链接进行重置密码：</h2><a href="http://127.0.0.1:8000/activate/forget/{0}">http://127.0.0.1:8000/activate/forget/{0}</a>'.format(
                code)
            # mail_status = mail.send_mail(subject=subject, message=text_content,
            #                              from_email='网络教育<{0}>'.format(settings.EMAIL_HOST_USER),
            #                              recipient_list=[self.email])
            msg = mail.EmailMultiAlternatives(subject=subject, body=text_content,
                                              from_email='网络教育<{0}>'.format(settings.EMAIL_HOST_USER), to=[self.email])
            msg.attach_alternative(content=html_content, mimetype='text/html')
            mail_status = msg.send()

            if mail_status:
                return True
            else:
                return False
