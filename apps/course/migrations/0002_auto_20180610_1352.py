# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-10 13:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(upload_to='courses/%Y/%m', verbose_name='封面'),
        ),
        migrations.AlterField(
            model_name='courseresource',
            name='download',
            field=models.FileField(upload_to='course/resource/%Y/%m', verbose_name='下载地址'),
        ),
    ]
