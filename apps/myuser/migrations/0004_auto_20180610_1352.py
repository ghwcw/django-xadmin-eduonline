# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-10 13:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0003_auto_20180610_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='image',
            field=models.ImageField(upload_to='banner/%Y/%m', verbose_name='轮播图片地址'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='image/default.jpg', upload_to='image/%Y/%m', verbose_name='上传的图片'),
        ),
    ]
