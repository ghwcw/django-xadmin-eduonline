import datetime
import json

from django.contrib import messages, auth
from django.contrib.auth import authenticate, hashers
from django.contrib.auth.backends import ModelBackend
from django.core.paginator import PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic.base import View
from pure_pagination import Paginator

from apps.course.models import Course
from apps.myuser.forms import LoginForm, RegisterForm, ForgetPwdForm, ResetPwdForm, UserCenUploadHeadimgForm, \
    UpdatePwdForm, UserCenInfoForm
from apps.myuser.models import UserProfile, EmailValiRecord, Banner
from apps.operation.models import UserCourse, UserFavorite, UserMessage
from apps.organization.models import CourseOrg, Teacher
from custbase.login_required import LoginRequiredMixin
from custbase.send_email import SendEmail
from eduonline import settings


class CustomBackend(ModelBackend):  # 继承ModelBackend类
    """
    自定义用户验证后端：支持用户名或邮箱登录。
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):

                return user
        except Exception as e:
            return None


class HomePageView(View):
    """
    基于通用类视图的首页(IP:port)
    """
    def get(self, request):
        return redirect(reverse('index'))


class IndexView(View):
    """
    基于通用类视图的首页(IP:port/index)
    """

    def get(self, request):

        try:
            username = request.session['username']
            succ_msg = request.session['succ_msg']
        except KeyError:
            username = ''
            succ_msg = ''

        # 消息数
        msg_counts = UserMessage.objects.filter(user=request.user.id, has_read=False).count()

        # 查询轮播图
        banners = Banner.objects.all()[:5]

        # 查询课程
        courses2 = Course.objects.order_by('-add_time')[:2]
        courseall = Course.objects.order_by('?')[2:8]

        # 查询机构
        orgs = CourseOrg.objects.order_by('?')[:15]

        return render(request, 'myuser/index.html', context={
            'username': username,
            'succ_msg': succ_msg,
            'msg_counts': msg_counts,
            'banners': banners,
            'courses2': courses2,
            'courseall': courseall,
            'orgs': orgs,
        })


class LoginView(View):
    """
    基于通用类视图的登录验证
    """

    def get(self, request):
        # 设置会话有效期，浏览器关闭失效
        request.session.set_expiry(0)
        remote_ip = request.META.get('REMOTE_ADDR', '获取IP失败')
        return render(request, 'myuser/login.html', context={'remote_ip': remote_ip})

    def post(self, request):
        global username, succ_msg

        form_data = LoginForm(request.POST)
        if form_data.is_valid():
            username = form_data.cleaned_data.get('username', None)
            password = form_data.cleaned_data.get('password', None)

            userobj = authenticate(username=username, password=password)
            if userobj is not None:
                if userobj.is_active:
                    auth.login(request, userobj)
                    succ_msg = '欢迎，登录成功！'
                    request.session['username'] = username
                    request.session['succ_msg'] = succ_msg

                    # 记录消息
                    UserMessage.objects.create(user=request.user.id, message='您在这时候登录过。', has_read=False)

                    return redirect(reverse('index'), username=username, succ_msg=succ_msg)
                else:
                    messages.error(request, '用户名未激活！')
                    return render(request, 'myuser/login.html', locals())
            else:
                messages.error(request, '用户名或密码不正确！')
                return render(request, 'myuser/login.html', locals())
        else:
            return render(request, 'myuser/login.html', context={'form_data': form_data})


class LogoutView(View):
    """
    退出
    """

    def get(self, request):
        auth.logout(request)
        return redirect(reverse('home'))


class RegisterView(View):
    """
    注册用户
    """

    def get(self, request):
        reg_form = RegisterForm()
        return render(request, template_name='myuser/register.html', context={'reg_form': reg_form})

    def post(self, request):
        reg_form = RegisterForm(request.POST)
        if reg_form.is_valid():
            email = reg_form.cleaned_data.get('email', '')
            if UserProfile.objects.filter(email=email):
                messages.error(request, '用户名已存在！')
                return render(request, 'myuser/register.html', {'reg_form': reg_form})
            password = reg_form.cleaned_data.get('password', '')
            user_profile = UserProfile()
            user_profile.username = email
            user_profile.email = email
            user_profile.password = hashers.make_password(password=password)  # 没有加盐
            user_profile.is_active = 0  # 还未邮箱验证，所以设为未激活0

            # 发送注册邮件
            send_email = SendEmail(email, send_type='register')
            send_status = send_email.send_acti_email()
            if send_status:
                user_profile.save()
                reg_msg = 'OK！邮件已发送，请登录您的邮箱按提示激活。。'
                return render(request, 'myuser/register.html', {'send_status': send_status, 'reg_msg': reg_msg})
            else:
                return render(request, 'myuser/register.html', {'reg_form': reg_form})
        else:
            return render(request, 'myuser/register.html', {'reg_form': reg_form})


class ActivateRegView(View):
    """
    邮箱验证
    """

    def get(self, request, activate_reg_code):
        email_vali = EmailValiRecord.objects.filter(code=activate_reg_code).last()
        if email_vali:
            email = email_vali.email
            user = UserProfile.objects.get(email=email)
            user.is_active = 1
            user.save()

            # 获取主机域名和端口
            # ip_port = settings.ALLOWED_HOSTS[0] + ':' + settings.ALLOWED_PORT[0]
            ip_port = request.META.get('SERVER_NAME') + ':' + request.META.get('SERVER_PORT')
            ip_port = ip_port.strip()

            # 记录消息
            UserMessage.objects.create(user=request.user.id, message='欢迎注册。', has_read=False)

            return HttpResponse('<h1>✔激活成功☞<a href="http://{0}/myuser/login">返回登录页面</a></h1>'.format(ip_port))
        else:
            return HttpResponse('<h1>✘激活失败</h1>')


class ForgetPwdView(View):
    """
    忘记密码
    """

    def get(self, request):
        forget_pwd_form = ForgetPwdForm()
        return render(request, 'myuser/forgetpwd.html', context={'forget_pwd_form': forget_pwd_form})

    def post(self, request):
        forget_pwd_form = ForgetPwdForm(request.POST)
        if forget_pwd_form.is_valid():
            email = forget_pwd_form.cleaned_data.get('email', '')
            user = UserProfile.objects.filter(email=email)
            if not user:
                messages.error(request, '用户名不存在！')
                return render(request, 'myuser/forgetpwd.html', {'forget_pwd_form': forget_pwd_form})

            # 发送重置密码邮件
            send_email = SendEmail(email, send_type='forget')
            send_status = send_email.send_acti_email()
            if send_status:
                forget_msg = 'OK！邮件已发送，请登录您的邮箱按提示重置密码。。'
                return render(request, 'myuser/forgetpwd.html', {'send_status': send_status, 'forget_msg': forget_msg})
            else:
                return render(request, 'myuser/forgetpwd.html', {'forget_pwd_form': forget_pwd_form})
        else:
            return render(request, 'myuser/forgetpwd.html', {'forget_pwd_form': forget_pwd_form})


class ActivateForgetView(View):
    """
    邮箱重置密码验证
    """

    def get(self, request, activate_forget_code):
        email_vali = EmailValiRecord.objects.filter(code=activate_forget_code).last()

        # 获取主机域名和端口
        # ip_port = settings.ALLOWED_HOSTS[0] + ':' + settings.ALLOWED_PORT[0]
        ip_port = request.META.get('SERVER_NAME') + ':' + request.META.get('SERVER_PORT')
        ip_port = ip_port.strip()

        if email_vali:
            return HttpResponse(
                '<h1>✔验证成功☞<a href="http://{0}/myuser/reset-pwd/{1}">立即重置密码</a></h1>'.format(
                    ip_port, activate_forget_code))
        else:
            return HttpResponse('<h1>✘验证失败</h1>')


class ResetPwdView(View):
    """
    重置密码
    """

    def get(self, request, email_code):
        email_vali = EmailValiRecord.objects.filter(code=email_code).last()
        if email_vali:
            reset_email = email_vali.email
            return render(request, 'myuser/password_reset.html', context={'reset_email': reset_email})
        else:
            return HttpResponse('<h1>未进行邮箱验证，不能修改密码！</h1>')

    def post(self, request):
        reset_pwd_form = ResetPwdForm(request.POST)
        if reset_pwd_form.is_valid():
            email = reset_pwd_form.cleaned_data.get('email', '')
            pwd1 = reset_pwd_form.cleaned_data.get('password1', '')
            pwd2 = reset_pwd_form.cleaned_data.get('password2', '')
            if pwd1 != pwd2:
                return render(request, 'myuser/password_reset.html', context={'msg': '错误：两次输入的密码不一致，请重新输入。'})
            else:
                user = UserProfile.objects.get(email=email)
                user.password = hashers.make_password(password=pwd1)
                user.save()

                # 记录消息，这里波许判断是否登陆
                user_id = UserProfile.objects.get(email=email).id
                if user_id:
                    UserMessage.objects.create(user=user_id, message='修改密码成功。', has_read=False)

                # 获取主机域名和端口
                # ip_port = settings.ALLOWED_HOSTS[0] + ':' + settings.ALLOWED_PORT[0]
                ip_port = request.META.get('SERVER_NAME') + ':' + request.META.get('SERVER_PORT')
                ip_port = ip_port.strip()

                return HttpResponse('<h1>密码修改成功！<<<a href="http://{0}/myuser/login">请返回登录页面</a></h1>'.format(ip_port))
        return render(request, 'myuser/password_reset.html', context={'reset_pwd_form': reset_pwd_form})


class UserCenInfoView(LoginRequiredMixin, View):
    """
    个人中心-个人资料
    """

    def get(self, request):
        # 若未登录
        # if not request.user.is_authenticated():
        #     return redirect(reverse('myuser:login'))

        try:
            username = request.session['username']
            succ_msg = request.session['succ_msg']
        except KeyError:
            username = ''
            succ_msg = ''

        # 消息数
        msg_counts = UserMessage.objects.filter(user=request.user.id, has_read=False).count()

        return render(request, 'usercenter/usercenter-info.html', context={
            'username': username,
            'succ_msg': succ_msg,
            'msg_counts': msg_counts,
        })

    def post(self, request):
        """
        保存个人资料
        :param request:
        :return:
        """
        # 若未登录
        # if not request.user.is_authenticated():
        #     return redirect(reverse('myuser:login'))

        info_form = UserCenInfoForm(request.POST, instance=request.user)
        if info_form.is_valid():
            info_form.save()

            # 记录消息
            UserMessage.objects.create(user=request.user.id, message='个人资料保存成功。', has_read=False)

            return JsonResponse(data={'status': 'success'})
        else:
            return JsonResponse(data={'status': 'fail', 'msg': '✘出错：请检查填写内容是否合法☹'})


class UserCenUploadHeadimgView(LoginRequiredMixin, View):
    """
    个人中心-用户头像修改
    """

    def post(self, request):
        # 若未登录
        # if not request.user.is_authenticated():
        #     return redirect(reverse('myuser:login'))

        try:
            username = request.session['username']
            succ_msg = request.session['succ_msg']
        except KeyError:
            username = ''
            succ_msg = ''

        # 修改头像，使用ModelForm快捷保存，需要传入实例参数instance=request.user
        headimg_form = UserCenUploadHeadimgForm(data=request.POST, files=request.FILES, instance=request.user)
        if headimg_form.is_valid():
            headimg_form.save()

            # 记录消息
            UserMessage.objects.create(user=request.user.id, message='修改头像成功。', has_read=False)

        return render(request, 'usercenter/usercenter-info.html', context={
            'username': username,
            'succ_msg': succ_msg,
        })


class UserCenUpdatePwdView(LoginRequiredMixin, View):
    """
    个人中心-修改密码
    """

    def post(self, request):
        # 若未登录
        # if not request.user.is_authenticated():
        #     return redirect(reverse('myuser:login'))

        update_pwd_form = UpdatePwdForm(request.POST)
        if update_pwd_form.is_valid():
            password1 = update_pwd_form.cleaned_data.get('password1', '')
            password2 = update_pwd_form.cleaned_data.get('password2', '')
            if password1 != password2:
                return JsonResponse({'status': 'fail', 'msg': '两次输入的密码不一致！'})
            user = request.user
            user.password = hashers.make_password(password1)
            user.save()

            # 记录消息
            UserMessage.objects.create(user=request.user.id, message='修改密码成功。', has_read=False)

            return JsonResponse({'status': 'success', 'msg': '密码修改成功！'})
        else:
            json_str = json.dumps(update_pwd_form.errors)
            return HttpResponse(json_str, content_type='application/json')


class UserCenSendEmailcodeView(LoginRequiredMixin, View):
    """
    个人中心-发送邮箱验证码
    """

    def get(self, request):
        # 若未登录
        # if not request.user.is_authenticated():
        #     return redirect(reverse('myuser:login'))

        email = request.GET.get('email', '')

        # 判断email是否已绑定
        if UserProfile.objects.filter(email=email):
            return JsonResponse(data={'email': '该邮箱已被绑定！'})
        # 发送邮件验证码
        sm = SendEmail(email, 'update_email')
        is_ok = sm.send_vali_emailcode()
        if is_ok:
            return JsonResponse(data={'status': 'success'})
        else:
            return JsonResponse(data={'status': 'fail'})


class UserCenUpdateEmailDoneView(LoginRequiredMixin, View):
    """
    个人中心-修改邮箱完成
    """

    def post(self, request):
        # 若未登录
        # if not request.user.is_authenticated():
        #     return redirect(reverse('myuser:login'))

        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        record = EmailValiRecord.objects.filter(email=email, code=code, send_type='update_email').last()
        if record:
            # 有效期2分钟
            now_time = datetime.datetime.now()
            send_time_delta = record.send_time + datetime.timedelta(minutes=2)
            if now_time > send_time_delta:
                return JsonResponse({'status': 'fail', 'msg': '验证码已过期，请重新验证'})

            # 开始更改邮箱
            user = request.user
            user.email = email
            user.save()

            # 记录消息
            UserMessage.objects.create(user=request.user.id, message='修改邮箱成功。', has_read=False)

            return JsonResponse({'status': 'success'})

        else:
            return JsonResponse({'status': 'fail', 'msg': '验证码出错，请重新验证'})


class UserCenCoursesView(LoginRequiredMixin, View):
    """
    个人中心-我的课程
    """

    def get(self, request):
        # 若未登录
        # if not request.user.is_authenticated():
        #     return redirect(reverse('myuser:login'))

        try:
            username = request.session['username']
            succ_msg = request.session['succ_msg']
        except KeyError:
            username = ''
            succ_msg = ''

        # 查询用户课程
        user_objs = UserCourse.objects.select_related('course').filter(user=request.user)
        courses = (user_obj.course for user_obj in user_objs)  # 使用了生成器
        # 消息数
        msg_counts = UserMessage.objects.filter(user=request.user.id, has_read=False).count()

        return render(request, 'usercenter/usercenter-mycourse.html', context={
            'username': username,
            'succ_msg': succ_msg,
            'courses': courses,
            'msg_counts': msg_counts,
        })


class UserCenFavOrgView(LoginRequiredMixin, View):
    """
    个人中心-我的收藏机构
    """

    def get(self, request):
        # 若未登录
        # if not request.user.is_authenticated():
        #     return redirect(reverse('myuser:login'))

        try:
            username = request.session['username']
            succ_msg = request.session['succ_msg']
        except KeyError:
            username = ''
            succ_msg = ''

        # 查询收藏机构
        user_favs = UserFavorite.objects.select_related('user').filter(user=request.user, fav_type=2)
        org_ids = (user_fav.fav_id for user_fav in user_favs)

        org_id_list = []
        for org_id in org_ids:
            org_id_list.append(org_id)

        orgs = CourseOrg.objects.filter(id__in=org_id_list)
        # 消息数
        msg_counts = UserMessage.objects.filter(user=request.user.id, has_read=False).count()

        return render(request, 'usercenter/usercenter-fav-org.html', context={
            'username': username,
            'succ_msg': succ_msg,
            'orgs': orgs,
            'msg_counts': msg_counts,
        })


class UserCenFavTeacherView(LoginRequiredMixin, View):
    """
    个人中心-我的收藏教师
    """

    def get(self, request):
        # 若未登录
        # if not request.user.is_authenticated():
        #     return redirect(reverse('myuser:login'))

        try:
            username = request.session['username']
            succ_msg = request.session['succ_msg']
        except KeyError:
            username = ''
            succ_msg = ''

        # 查询收藏教师
        user_favs = UserFavorite.objects.select_related('user').filter(user=request.user, fav_type=3)
        teacher_ids = (user_fav.fav_id for user_fav in user_favs)

        teacher_id_list = []
        for teacher_id in teacher_ids:
            teacher_id_list.append(teacher_id)

        teachers = Teacher.objects.filter(id__in=teacher_id_list)
        # 消息数
        msg_counts = UserMessage.objects.filter(user=request.user.id, has_read=False).count()

        return render(request, 'usercenter/usercenter-fav-teacher.html', context={
            'username': username,
            'succ_msg': succ_msg,
            'teachers': teachers,
            'msg_counts': msg_counts,
        })


class UserCenFavCourseView(LoginRequiredMixin, View):
    """
    个人中心-我的收藏课程
    """

    def get(self, request):
        # 若未登录
        # if not request.user.is_authenticated():
        #     return redirect(reverse('myuser:login'))

        try:
            username = request.session['username']
            succ_msg = request.session['succ_msg']
        except KeyError:
            username = ''
            succ_msg = ''

        # 查询用户课程
        user_objs = UserCourse.objects.select_related('course').filter(user=request.user)
        courses = (user_obj.course for user_obj in user_objs)  # 使用了生成器
        # 消息数
        msg_counts = UserMessage.objects.filter(user=request.user.id, has_read=False).count()

        return render(request, 'usercenter/usercenter-fav-course.html', context={
            'username': username,
            'succ_msg': succ_msg,
            'courses': courses,
            'msg_counts': msg_counts,
        })


class UserCenMsgView(LoginRequiredMixin, View):
    """
    个人中心-我的消息
    """

    def get(self, request):
        # 若未登录
        # if not request.user.is_authenticated():
        #     return redirect(reverse('myuser:login'))

        try:
            username = request.session['username']
            succ_msg = request.session['succ_msg']
        except KeyError:
            username = ''
            succ_msg = ''

        # 查询我的消息
        messages = UserMessage.objects.filter(user=request.user.id).order_by('-add_time')
        # 消息数
        msg_counts = UserMessage.objects.filter(user=request.user.id, has_read=False).count()

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(messages, 10, request=request)
        page_obj = p.page(page)

        return render(request, 'usercenter/usercenter-message.html', context={
            'username': username,
            'succ_msg': succ_msg,
            'page_obj': page_obj,
            'msg_counts': msg_counts,
        })

    def post(self, request):
        """
        将消息标记为已读
        :param request:
        :return:
        """
        msg_id = int(request.POST.get('msg_id', '0'))
        has_read = request.POST.get('has_read', 'False')
        one_key = request.POST.get('one_key', '')

        if one_key:
            UserMessage.objects.filter(user=request.user.id).update(has_read=True)
            return JsonResponse({'status': 'success'})

        if msg_id:
            msg = get_object_or_404(UserMessage, id=msg_id)
            if has_read == 'False':
                msg.has_read = 'True'
                msg.save()
                return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': ''})
