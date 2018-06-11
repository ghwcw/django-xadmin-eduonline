from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import View, TemplateView

from apps.myuser.forms import LoginForm
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


class HomePageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['flag'] = None
        return context


class IndexView(TemplateView):
    """
    基于通用类视图的首页
    """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['username'] = username
        context['succ_msg'] = succ_msg
        return context


class LoginView(View):
    """
    基于通用类视图的登录验证
    """

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        global username, succ_msg

        form_data = LoginForm(request.POST)
        if form_data.is_valid():
            username = form_data.cleaned_data.get('username', None)
            password = form_data.cleaned_data.get('password', None)

            userobj = authenticate(username=username, password=password)
            if userobj is not None:
                auth.login(request, userobj)
                succ_msg = '欢迎，登录成功！'
                request.session['username'] = username
                request.session['succ_msg'] = succ_msg
                return redirect(reverse('index'), username=username, succ_msg=succ_msg)
            else:
                messages.error(request, '用户名或密码不正确！')
                return render(request, 'login.html', locals())
        else:
            return render(request, 'login.html', context={'form_data': form_data})


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect(reverse('home'))



# ******************************************************************************************* #


# def index(request):
#     """
#     首页视图
#     :param request:
#     :return:
#     """
#     username = request.session.get('username', None)
#     succ_msg = request.session.get('succ_msg', None)
#     return render(request, 'index.html', context={'username': username, 'succ_msg': succ_msg})
#
#
# def user_login(request):
#     """
#     用户登录视图
#     :param request:
#     :return:
#     """
#     global username, succ_msg
#
#     if request.method == 'POST':
#         username = request.POST.get('username', None)
#         password = request.POST.get('password', None)
#         userobj = authenticate(username=username, password=password)
#         if userobj is not None:
#             login(request, userobj)
#             succ_msg = '欢迎，登录成功！'
#             request.session['username'] = username
#             request.session['succ_msg'] = succ_msg
#             return redirect(reverse('index'), username=username, succ_msg=succ_msg)
#         else:
#             messages.error(request, '用户名或密码不正确！')
#             return render(request, 'login.html', locals())
#
#     elif request.method == 'GET':
#         return render(request, 'login.html')
