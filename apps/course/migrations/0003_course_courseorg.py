# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-21 10:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_auto_20180620_1131'),
        ('course', '0002_auto_20180610_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='courseorg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='organization.CourseOrg', verbose_name='课程机构'),
        ),
    ]
