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
sys.path.append(os.path.join(BASE_DIR, 'extraapps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# 产品密钥。创建Django项目时自动分配的产品密钥，请使用原自动分配的产品密钥替换此行！！
SECRET_KEY = '81$k-x)bqrs4!!kjyifja)g=^zi*j@62$&n_c%4&ic*ni5q%dd'

# 上线时必须将DEBUG设为False
DEBUG = False

# 可指定主机，若元素为'*'，表示所有同一局域网内的网络均可被访问
# 主机和端口不要轻易改动
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
ALLOWED_PORT = ['70', '*']

# App加载
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'apps.myuser',
    'apps.course',
    'apps.organization',
    'apps.operation',
    'xadmin',
    'crispy_forms',
    'captcha',
    'pure_pagination',
]

# 自定义的用户表
AUTH_USER_MODEL = 'myuser.UserProfile'

# 自定义的用户验证后端类
AUTHENTICATION_BACKENDS = ['apps.myuser.views.CustomBackend']

# 中间件
MIDDLEWARE = [
    # 'django.middleware.cache.UpdateCacheMiddleware',          # 缓存配置，必须排在第一个
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',     # 依赖于会话Session
    'django.middleware.clickjacking.XFrameOptionsMiddleware',   # 防止点击劫持
    # 'custbase.http.SetRemoteAddrFromForwardedFor',
    # 'django.middleware.cache.FetchFromCacheMiddleware',       # 缓存配置，必须在最后一个
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
                'django.template.context_processors.media',
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

# 密码验证
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
LANGUAGE_CODE = 'en-us'       # 系统语言。中文简体是'zh-hans'(此时USE_I18N必须为True)，Admin后台管理系统的页面语言随之改变
TIME_ZONE = 'Asia/Shanghai'   # 时区
USE_I18N = True               # 翻译
USE_L10N = True               # 本地化
USE_TZ = False                # 若使用了本地时间，必须设为False!!(默认值True)

# 邮件服务配置
EMAIL_HOST = 'smtp.qq.com'  # 发送者邮箱服务器
EMAIL_PORT = 25
EMAIL_HOST_USER = 'wang@qq.com'  # 发送者用户名（邮箱地址）
EMAIL_HOST_PASSWORD = '123456'  # 发送者密码
EMAIL_USE_SSL = False

# 静态文件配置 (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
# 静态文件的访问目录，自动指向"STATIC_ROOT"或"STATICFILES_DIRS"的目录值。用于程序中，如{{static '静态文件指向目录下的子路径'}}
# 这里的静态文件URL，即/static/通常用于 Apache 或 Nginx 配置文件中的静态文件访问配置（生产策略!）
# 模板调用示例：{% static 'images/123.jpg' %}
STATIC_URL = '/static/'
# 静态文件的生产环境根目录！仅用于生产！当运行"python manage.py collectstatic"的时候，会将STATICFILES_DIRS以及各app中static的所有的文件复制收集到STATIC_ROOT
# 把这些文件放到一起是为了用Apache、Nginx等上线部署的时候更方便
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# 公共静态文件目录，但不能与STATIC_ROOT冲突！
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'commstatic')]

# 媒体文件(用户上传的文件)配置，类似于上面的静态文件配置
# 不能像静态文件那样调用，而是先在settings的"TEMPLATES"中的"context_processors"添加：'django.template.context_processors.media'
# (调试策略！手动指定视图访问media文件目录，部署生产请注释掉) 添加URL路由，如"url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})"
# 模板调用示例：{{ MEDIA_URL }}{{ modelobj.fieldname }}
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 缓存后端配置（Django支持许多开箱即用的缓存后端）
# Django默认缓存后端是本地内存（LocMemCache）。虚拟DummyCache用于开发（实际上并不缓存，它只是实现缓存接口而不做任何事情。）
# Django支持的缓存类型：Memcached（MemcachedCache）、本地内存（LocMemCache）、数据库（DatabaseCache）、文件（FileBasedCache）、虚拟（DummyCache）
# Memcached缓存数据库下载与安装教程：http://www.runoob.com/memcached/window-install-memcached.html（菜鸟教程提供）
# 下载安装Memcached本身后，您还需要安装其依赖模块。最常见的两个依赖模块是python-memcached和pylibmc（pip安装）
# 设置缓存后端后，使用缓存的最简单方法是缓存整个站点
# 在中间件列表中的[开头]和[末尾]添加如下2个中间件：'django.middleware.cache.UpdateCacheMiddleware'和'django.middleware.cache.FetchFromCacheMiddleware'
# 测试，进入Python shell：
# >>> from django.core.cache import cache
# >>> cache.set('test', 'successful', 60)           第一个参数是key，第二个参数value，第三个参数是过期时间（秒）
# >>> cache.get('test')
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',       # 取决于您选择的Memcached绑定
#         'LOCATION': ['127.0.0.1:11211', ],              # 缓存后端服务器位置，支持分布式，可多个
#         'TIMEOUT': 30,                                  # 缓存超时，默认300s
#         'OPTIONS': {
#             'server_max_value_length': 2*1024*1024,     # 缓存最大值（这里的键值根据缓存类型不同而变化，一般默认也可）
#         },
#         'CACHE_MIDDLEWARE_ALIAS': 'DJCACHE',            # 用于存储的缓存别名
#         'CACHE_MIDDLEWARE_SECONDS': 30,                 # 每个页面应缓存的秒数
#         'CACHE_MIDDLEWARE_KEY_PREFIX': '',              # 缓存键前缀。如果使用相同的Django在多个站点之间共享缓存，将其设置为站点名称（或其他）以防止发生密钥冲突
#     }
# }

# 会话使用的缓存（CACHES），默认"default"
# SESSION_CACHE_ALIAS = "default"
# 会话缓存期限，默认2周
# SESSION_COOKIE_AGE = 1209600
# 会话生存期设置，浏览器关闭，则会话失效（可能对Chrome浏览器无效）。在登录视图get请求中添加语句"request.session.set_expiry(0)"，对Chrome会有效
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 默认False
