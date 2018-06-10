from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse

from apps.myuser.models import UserProfile


class CustomBackend(ModelBackend):
    """
    自定义用户登录验证：支持用户名或邮箱登录。
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


def index(request):
    """
    首页视图
    :param request:
    :return:
    """
    return render(request, 'index.html', context={'username': username, 'succ_msg': succ_msg})


def user_login(request):
    """
    用户登录视图
    :param request:
    :return:
    """
    global username, succ_msg
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        userobj = authenticate(username=username, password=password)
        if userobj is not None:
            login(request, userobj)
            succ_msg = '欢迎，登录成功！'
            return redirect(reverse('index'))
        else:
            messages.error(request, '用户名或密码不正确！')
            return render(request, 'login.html', locals())

    elif request.method == 'GET':
        return render(request, 'login.html')
