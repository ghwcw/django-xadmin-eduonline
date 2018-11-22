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
from django.http import HttpResponse
from django.utils.translation import gettext

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduonline.settings')
django.setup()


def my_view():
    output = gettext("Welcome to my site.")
    return HttpResponse(output)


print(my_view().getvalue())
