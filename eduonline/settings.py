"""
Django settings for eduonline project.

Generated by 'django-admin startproject' using Django 1.11.13.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# 这里用到了python中一个神奇的变量"__file__"， 这个变量可以获取到当前文件的路径（含文件名）
# 再来一个os.path.dirname()就是获得上一级目录
# "BASE_DIR"就是工程根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 如果包含外部APP，Mark成Source Root后可能还需要添加如下配置，否则运行manage.py会报错No module named 'xx'
# "extraapps"是外部APP上级目录包（Mark成Source Root）
sys.path.insert(0, os.path.join(BASE_DIR, 'extraapps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# 产品密钥。创建Django项目时自动分配的产品密钥，请使用原自动分配的产品密钥替换此行！！
SECRET_KEY = '81$k-x)bqrs4!!kjyifja)g=^zi*j@62$&n_c%4&ic*ni5q%dd'

# 上线时必须将DEBUG设为False
DEBUG = True

# 可指定主机，若元素为'*'，表示所有同一局域网内的网络均可访问
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# App加载
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.myuser',
    'apps.course',
    'apps.organization',
    'apps.operation',
    'xadmin',
    'crispy_forms',
]

# 自定义的用户表
AUTH_USER_MODEL = 'myuser.UserProfile'

# 自定义的用户验证后端类
# AUTHENTICATION_BACKENDS = ['apps.myuser.views.CustomBackend', ]

# 中间件
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'eduonline.urls'  # 这里需要据实修改

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'eduonline.wsgi.application'  # 这里需要据实修改

# 数据库
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# 用户验证
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 国际化
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = 'zh-hans'  # 中文简体是'zh-hans'，Admin后台管理系统的页面语言随之改变

# 本地时间
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False  # 若使用了本地时间，必须设为False!!(默认值True)

# 邮件服务配置
EMAIL_HOST = 'xxx@xx.com'  # 发送者邮箱服务器
EMAIL_PORT = 25
EMAIL_HOST_USER = ''  # 发送者用户名（邮箱地址）
EMAIL_HOST_PASSWORD = ''  # 发送者密码
EMAIL_USE_SSL = False

# 静态文件配置 (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# 静态文件的URL名称，用于程序中，如{{static '路径'}}
STATIC_URL = '/static/'

# 静态文件的生产环境根目录，当运行"python manage.py collectstatic"的时候，会将STATICFILES_DIRS以及各app中static的所有的文件复制收集到STATIC_ROOT
# 把这些文件放到一起是为了用Apache等上线部署的时候更方便
# STATIC_ROOT=os.path.join(BASE_DIR, 'collected_statics').replace('\\', '/')

# 静态文件的公用目录，但不能与STATIC_ROOT冲突！
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# 上传媒体文件
MEDIA_URL = '/static/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')

# 缓存配置，下方一般限开发者用
# 可以缓存于内存（locmem.LocMemCache）或文件（filebased.FileBasedCache）
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
