#!/usr/bin/env python
# coding:utf-8
"""
-------------------------------------------------------------
    Creator : 汪春旺
       Date : 2018-06-22
    Project : eduonline
   FileName : courseurl.py
Description : 
-------------------------------------------------------------
"""
from django.conf.urls import url

from apps.course.views import CourseListView, CourseDetailView, CourseVideoView, play_video, CourseStudyView, \
    AllCourseRss, AllCourseAtom

urlpatterns = [
    url(r'^course-list/$', CourseListView.as_view(), name='course_list'),
    url(r'^course-detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    # “开始学习”页url
    url(r'^course-study/$', CourseStudyView.as_view(), name='course_study'),
    url(r'^course-video/(?P<course_id>\d+)/$', CourseVideoView.as_view(), name='course_video'),
    url(r'^video-play/$', play_video, name='video_play'),

    url(r'^course-rss/$', AllCourseRss(), name='course_rss'),
    url(r'^course-atom/$', AllCourseAtom(), name='course_atom'),

]
