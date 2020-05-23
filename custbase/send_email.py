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
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduonline.settings')     # environ字典
# import django
# django.setup()

import random
from _md5 import md5
from django.core import mail

from apps.myuser.models import EmailValiRecord
from eduonline import settings


class SendEmail(object):
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

    @staticmethod
    def create_random_nums(n=4):
        """
        随机取出n个数字字符
        """
        string = '0123456789'
        res_str = ''
        for _ in range(n):
            res_str += string[random.randint(0, len(string) - 1)]
        return res_str

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

        # 获取主机域名和端口
        ip_port = settings.ALLOWED_HOSTS[0] + ':' + settings.ALLOWED_PORT[0]
        ip_port = ip_port.strip()

        if self.send_type == 'register':
            subject = '网络教育在线注册激活'
            text_content = '请确认邮件后，点击该链接进行账号激活：http://{0}/activate/reg/{1}'.format(ip_port, code)
            html_content = '<h2>请确认邮件后，点击下方链接进行账号激活：</h2><a href="http://{0}/activate/reg/{1}">http://{0}/activate/reg/{1}</a>'.format(
                ip_port, code)
            # mail_status = mail.send_mail(subject=subject, message=text_content,
            #                              from_email='网络教育<{0}>'.format(settings.EMAIL_HOST_USER),
            #                              recipient_list=[self.email])
            try:
                msg = mail.EmailMultiAlternatives(subject=subject, body=text_content,
                                                  from_email='网络教育<{0}>'.format(settings.EMAIL_HOST_USER), to=[self.email])
                msg.attach_alternative(content=html_content, mimetype='text/html')
                mail_status = msg.send()
            except TimeoutError:
                raise Exception('发送邮件失败！请检查：1.网络是否正常；2.邮箱服务器、用户、密码等等是否正确。')

            if mail_status:
                return True
            else:
                return False

        elif self.send_type == 'forget':
            subject = '网络教育在线重置密码'
            text_content = '请确认邮件后，点击该链接进行重置密码：http://{0}/activate/resetpwd/{1}'.format(ip_port, code)
            html_content = '<h2>请确认邮件后，点击下方链接进行重置密码：</h2><a href="http://{0}/activate/forget/{1}">http://{0}/activate/forget/{1}</a>'.format(
                ip_port, code)
            # mail_status = mail.send_mail(subject=subject, message=text_content,
            #                              from_email='网络教育<{0}>'.format(settings.EMAIL_HOST_USER),
            #                              recipient_list=[self.email])
            try:
                msg = mail.EmailMultiAlternatives(subject=subject, body=text_content,
                                                  from_email='网络教育<{0}>'.format(settings.EMAIL_HOST_USER), to=[self.email])
                msg.attach_alternative(content=html_content, mimetype='text/html')
                mail_status = msg.send()
            except TimeoutError:
                raise Exception('发送邮件失败！请检查：1.网络是否正常；2.邮箱服务器、用户、密码等等是否正确。')

            if mail_status:
                return True
            else:
                return False

    def send_vali_emailcode(self):
        """
        产生4位数字验证码
        :return:
        """
        email_valid = EmailValiRecord()
        code = SendEmail.create_random_nums()
        email_valid.code = code
        email_valid.email = self.email
        email_valid.send_type = self.send_type
        email_valid.save()

        if self.send_type == 'update_email':
            subject = '网络教育在线修改邮箱'
            text_content = '您的邮箱验证码为(请不要告诉他人)：{0}'.format(code)
            html_content = '<h2>您的邮箱验证码为(请不要告诉他人)：</h2> {0}'.format(code)
            # mail_status = mail.send_mail(subject=subject, message=text_content,
            #                              from_email='网络教育<{0}>'.format(settings.EMAIL_HOST_USER),
            #                              recipient_list=[self.email])
            try:
                msg = mail.EmailMultiAlternatives(subject=subject, body=text_content,
                                                  from_email='网络教育<{0}>'.format(settings.EMAIL_HOST_USER), to=[self.email])
                msg.attach_alternative(content=html_content, mimetype='text/html')
                mail_status = msg.send()
            except TimeoutError:
                raise Exception('发送邮件失败！请检查：1.网络是否正常；2.邮箱服务器、用户、密码等等是否正确。')

            if mail_status:
                return True
            else:
                return False


# if __name__ == '__main__':
#     m = SendEmail('wongnina@vip.qq.com', 'update_email')
#     m.send_vali_emailcode()

