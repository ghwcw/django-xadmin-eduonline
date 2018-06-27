#!/usr/bin/env python
# coding:utf-8
"""
-------------------------------------------------------------
    Creator : 汪春旺
       Date : 2018-06-10
    Project : eduonline
   FileName : myuserurl.py
Description : 
-------------------------------------------------------------
"""
from django.conf.urls import url
from apps.myuser.views import LoginView, LogoutView, RegisterView, ForgetPwdView, ResetPwdView, \
    UserCenInfoView, UserCenUploadHeadimgView

# app_name = 'myuser'

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^forget-pwd/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset-pwd/(?P<email_code>.*)/$', ResetPwdView.as_view(), name='reset_pwd'),
    url(r'^reset-pwd-post/$', ResetPwdView.as_view(), name='reset_pwd_post'),

    # 个人信息中心
    url(r'^usercen-info/$', UserCenInfoView.as_view(), name='usercen_info'),
    url(r'^usercen-upload-headimg/$', UserCenUploadHeadimgView.as_view(), name='usercen_upload_headimg'),

]
