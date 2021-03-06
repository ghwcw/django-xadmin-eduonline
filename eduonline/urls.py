"""eduonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib.sitemaps.views import sitemap
from django.views.defaults import page_not_found
from django.views.generic import TemplateView
from django.views.static import serve

import xadmin
from apps.course.views import CourseSitemap
from apps.myuser.views import IndexView, HomePageView, ActivateRegView, ActivateForgetView
from eduonline import settings
# from mydemo.mytest import signal_sender

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),

    # 首页相关
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^index/$', IndexView.as_view(), name='index'),
    url(r'^test/$', TemplateView.as_view(template_name='test/test.html')),

    # 用户相关
    url(r'^myuser/', include('apps.myuser.myuserurl', namespace='myuser')),
    url(r'^captcha/', include('captcha.urls')),
    # 邮箱验证
    url(r'^activate/reg/(?P<activate_reg_code>.*)/$', ActivateRegView.as_view(), name='activate_reg'),
    url(r'^activate/forget/(?P<activate_forget_code>.*)/$', ActivateForgetView.as_view(), name='activate_forget'),

    # 用户上传文件（调试策略）
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    # 静态文件，一般用不到
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    # 机构相关
    url(r'^org/', include('apps.organization.orgurl', namespace='org')),

    # 用户操作相关
    url(r'^oper/', include('apps.operation.operurl', namespace='oper')),

    # 课程相关
    url(r'^course/', include('apps.course.courseurl', namespace='course')),

    # 站点地图
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': {'course': CourseSitemap}}, name='sitemap'),

    # 信号测试
    # url(r'^signal/$', signal_sender),

]

# 自定义的处理全局404，500页面视图（对应的视图路径）
handler404 = 'apps.operation.views.page_not_found'
handler500 = 'apps.operation.views.server_error'

# 系统默认的处理全局404，500页面视图（对应的视图路径）
# handler404 = 'django.views.defaults.page_not_found'
# handler500 = 'django.views.defaults.server_error'
handler400 = 'django.views.defaults.bad_requuest'
handler403 = 'django.views.defaults.permission_denied'
