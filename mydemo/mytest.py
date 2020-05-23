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
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduonline.settings')
django.setup()

import timeit
import datetime
from django.core.mail import send_mail
from django.core.signals import request_finished
from django.dispatch import receiver, Signal
from django.http import HttpResponse
from django.utils.translation import gettext

from apps.course.models import Course
# def my_view():
#     output = gettext("Welcome to my site.")
#     return HttpResponse(output)
#
#
# print(my_view().getvalue())

# ---------------------------------------------- #

# subject = 'Django测试'
# message = '这是测试邮件，请忽略'
# html_message = '<h2 style="color:red;">这是测试邮件，请忽略</h2>'
# res = send_mail(subject=subject, message=message, from_email='Django管理员<wangchunwang@dhcc.com.cn>',
#                 recipient_list=['wcwnina@foxmail.com'],
#                 html_message=html_message)
#
# if res:
#     print('发送成功')
# else:
#     print('发送失败')

# test_signal = Signal(['hostname', 'msg', 'time'])

# ---------------------------------------------- #

# # 发送信号
# def signal_sender(request):
#     hostname = request.get_host()
#     msg = 'Django Signal Test'
#     time = datetime.date.today()
#     test_signal.send(sender=signal_sender, hostname=hostname, msg=msg, time=time)     # 关键一行
#     return HttpResponse('200 OK')
#
#
# # 接收和处理信号
# @receiver(test_signal, sender=signal_sender)      # 装饰器把处理函数注册成接收器
# def signal_handler(sender, **kwargs):             # kwargs字典接收信号参数
#     print('接收到信号内容：{hostname}|"{msg}"|{time}'.format(hostname=kwargs['hostname'], msg=kwargs['msg'], time=kwargs['time']))
#

# ---------------------------------------------- #

# li = [11, 12, 13, 14, 15, 16, 17, 18, 19, 110]
#
#
# def bin_search(arr, find):
#     mid = len(arr) // 2
#     if len(arr) >= 1:
#         if find < arr[mid]:
#             bin_search(arr[:mid], find)
#         elif find > arr[mid]:
#             bin_search(arr[mid + 1:], find)
#         else:
#             # return mid
#             print(mid)
#     else:
#         # return '-1'
#         print("not found !")
#
#
# # recursion_search(li, 11)
# bin_search(li, 11)

# ---------------------------------------------- #

#
# class Foo():
#     def bar(self):
#         print('from parent class.')
#
#
# class Child(Foo):
#     def bar(self):
#         super(Child, self).bar()
#         print('from child class.')
#
#
# c = Child()
# c.bar()


class CourseTeacher():
    @classmethod
    def get_course_by_teacherid(cls, teacherid):
        """
        根据教师ID获取关联课程
        :param teacherid:
        :return:
        """
        courses = Course.objects.select_related('teacher').filter(teacher=teacherid)
        result = ''
        for course in courses:
            course_id = course.id
            course_name = course.name
            course_str = str(course_id) + '@' + course_name
            result = result + '^' + course_str

        if not courses: return '教师ID：' + str(teacherid) + '不存在！请核实。'
        return result, courses.count()



if __name__ == '__main__':
    print(CourseTeacher.get_course_by_teacherid(1))
    print(timeit.timeit(stmt='CourseTeacher.get_course_by_teacherid(1)', setup='from __main__ import CourseTeacher', number=100))



