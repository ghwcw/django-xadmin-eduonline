# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-04 21:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0011_course_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='courses/%Y/%m', verbose_name='封面'),
        ),
    ]
