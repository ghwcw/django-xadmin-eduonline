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
    UserCenInfoView, UserCenUploadHeadimgView, UserCenUpdatePwdView, UserCenSendEmailcodeView, \
    UserCenUpdateEmailDoneView, UserCenCoursesView, UserCenFavOrgView, UserCenFavCourseView, UserCenFavTeacherView, \
    UserCenMsgView

# app_name = 'myuser'

urlpatterns = [
    url(r'^myuser/$', LoginView.as_view(), name='myuser'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^forget-pwd/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset-pwd/(?P<email_code>.*)/$', ResetPwdView.as_view(), name='reset_pwd'),
    url(r'^reset-pwd-post/$', ResetPwdView.as_view(), name='reset_pwd_post'),

    # 个人信息中心
    url(r'^usercen-info/$', UserCenInfoView.as_view(), name='usercen_info'),
    url(r'^usercen-upload-headimg/$', UserCenUploadHeadimgView.as_view(), name='usercen_upload_headimg'),
    url(r'^usercen-update-pwd/$', UserCenUpdatePwdView.as_view(), name='usercen_update_pwd'),
    url(r'^usercen-send-emailcode/$', UserCenSendEmailcodeView.as_view(), name='usercen_send_emailcode'),
    url(r'^usercen-update-email-done/$', UserCenUpdateEmailDoneView.as_view(), name='usercen_update_email_done'),
    url(r'^usercen-mycourses/$', UserCenCoursesView.as_view(), name='usercen_mycourses'),
    url(r'^usercen-myfav-orgs/$', UserCenFavOrgView.as_view(), name='usercen_myfav_orgs'),
    url(r'^usercen-myfav-courses/$', UserCenFavCourseView.as_view(), name='usercen_myfav_courses'),
    url(r'^usercen-myfav-teachers/$', UserCenFavTeacherView.as_view(), name='usercen_myfav_teachers'),
    url(r'^usercen-mymsg/$', UserCenMsgView.as_view(), name='usercen_mymsg'),

]
