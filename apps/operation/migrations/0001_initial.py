# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-10 09:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=200, verbose_name='评论内容')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='course.Course', verbose_name='课程')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='评论用户')),
            ],
            options={
                'verbose_name': '课程评论表',
                'verbose_name_plural': '课程评论表',
            },
        ),
        migrations.CreateModel(
            name='UserAsk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='名字')),
                ('mobile', models.CharField(max_length=11, verbose_name='手机号')),
                ('course_name', models.CharField(max_length=50, verbose_name='课程名')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '用户咨询表',
                'verbose_name_plural': '用户咨询表',
            },
        ),
        migrations.CreateModel(
            name='UserCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='course.Course', verbose_name='课程')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户课程表',
                'verbose_name_plural': '用户课程表',
            },
        ),
        migrations.CreateModel(
            name='UserFavorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fav_type', models.IntegerField(choices=[(1, '课程'), (2, '课程机构'), (3, '教师')], verbose_name='收藏类型')),
                ('fav_id', models.IntegerField(default=1, verbose_name='收藏ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='收藏用户')),
            ],
            options={
                'verbose_name': '用户收藏表',
                'verbose_name_plural': '用户收藏表',
            },
        ),
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField(default=0, verbose_name='接收用户ID')),
                ('message', models.CharField(max_length=500, verbose_name='消息内容')),
                ('is_read', models.BooleanField(default=False, verbose_name='是否已读')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='消息发出时间')),
            ],
            options={
                'verbose_name': '用户消息表',
                'verbose_name_plural': '用户消息表',
            },
        ),
    ]
