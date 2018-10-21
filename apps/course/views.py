from django.db.models import Q
from django.http import JsonResponse, Http404, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, get_list_or_404

# Create your views here.
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger

from apps.course.models import Course, CourseResource
from apps.operation.models import UserFavorite, UserCourse, CourseComment, UserMessage
from apps.organization.models import CourseOrg


class CourseListView(View):
    """
    公开课导航列表页
    """

    def get(self, request):
        try:
            username = request.session['username']
            succ_msg = request.session['succ_msg']
        except KeyError:
            username = ''
            succ_msg = ''

        all_courses = Course.objects.all().order_by('-add_time')
        # 热门课推荐
        hot_courses = Course.objects.all().order_by('-fav_nums')[:3]

        # 搜索公开课
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_courses = all_courses.filter(Q(name__icontains=keywords) | Q(detail__icontains=keywords))

        # 筛选排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')

        course_nums = all_courses.count()

        # 消息数
        msg_counts = UserMessage.objects.filter(user=request.user.id, has_read=False).count()

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_courses, 6, request=request)
        page_obj = p.page(page)

        return render(request, 'course/course-list.html', context={
            'username': username,
            'succ_msg': succ_msg,
            'page_obj': page_obj,
            'sort': sort,
            'hot_courses': hot_courses,
            'course_nums': course_nums,
            'keywords': keywords,
            'msg_counts': msg_counts,
        })


class CourseDetailView(View):
    """
    课程详情
    """

    def get(self, request, course_id):
        try:
            username = request.session['username']
            succ_msg = request.session['succ_msg']
        except KeyError:
            username = ''
            succ_msg = ''

        course = get_object_or_404(Course, pk=course_id)
        # 功能同下：
        # try:
        #     course = Course.objects.get(pk=course_id)
        # except Course.DoesNotExist:
        #     raise Http404('找不到页面！')             # 抛出404异常
        #     # return HttpResponseNotFound('<h2>找不到页面！</h2>')    # 返回自定义页面

        # 点击量加1
        course.click_nums += 1
        course.save()

        # 相关课程
        tag = course.tag
        if tag:
            relate_course = Course.objects.filter(name__icontains=tag).exclude(pk=course.pk)[:2]
        else:
            relate_course = []

        # 判断是否收藏
        is_fav_course = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                is_fav_course = True

        is_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.courseorg.pk, fav_type=2):
                is_fav_org = True

        # 消息数
        msg_counts = UserMessage.objects.filter(user=request.user.id, has_read=False).count()

        return render(request, 'course/course-detail.html', context={
            'username': username,
            'succ_msg': succ_msg,
            'course': course,
            'relate_course': relate_course,
            'is_fav_course': is_fav_course,
            'is_fav_org': is_fav_org,
            'msg_counts': msg_counts,
        })


class CourseStudyView(View):
    """
    处理 “开始学习” 请求，并将数据记录到UserCourse表
    """
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({"status": "fail", "msg": "用户未登录"})

        course_id = request.POST.get('course_id', 0)
        if request.user and int(course_id) > 0:
            # 记录到用户课程
            if not UserCourse.objects.filter(user=request.user, course_id=course_id):
                UserCourse.objects.create(user=request.user, course_id=int(course_id))

            course = Course.objects.get(id=int(course_id))
            # 课程及其机构学习人数加1
            course.students += 1
            course.courseorg.students += 1
            course.save()
            course.courseorg.save()

            # 记录消息
            UserMessage.objects.create(user=request.user.id, message='您在这时学习了《%s》课程。' % course.name, has_read=False)

            return JsonResponse({"status": "success", "msg": "开启学习之旅..."})
        else:
            return JsonResponse({"status": "fail", "msg": "出错了！"})


class CourseVideoView(View):
    """
    “开始学习”--课程章节
    """

    def get(self, request, course_id):
        try:
            username = request.session['username']
            succ_msg = request.session['succ_msg']
        except KeyError:
            username = ''
            succ_msg = ''

        course = Course.objects.get(id=course_id)
        org_id = course.courseorg.id
        org = CourseOrg.objects.get(id=org_id)
        teacher = org.teacher_set.first()
        download_res = get_list_or_404(CourseResource)

        # 根据用户课程ID，查询出收藏过该课程的用户及其收藏的课程
        usercourse = UserCourse.objects.filter(course=course_id).first()
        if usercourse:
            user = usercourse.user
            course_id_list = UserCourse.objects.filter(user=user).values_list('course')
            usercourse_list = Course.objects.filter(id__in=course_id_list)[:3]
            # print(usercourse_list)
        else:
            usercourse_list = []

        # 消息数
        msg_counts = UserMessage.objects.filter(user=request.user.id, has_read=False).count()

        return render(request, 'course/course-video.html', context={
            'username': username,
            'succ_msg': succ_msg,
            'course_id': course_id,
            'course': course,
            'download_res': download_res,
            'teacher': teacher,
            'usercourse_list': usercourse_list,
            'msg_counts': msg_counts,
        })


def play_video(request):
    """
    “开始学习”--视频播放页
    """
    return render(request, 'course/videoplay.html')


class CourseCommentView(View):
    """
    “开始学习”--课程评论
    """

    def get(self, request, course_id):
        try:
            username = request.session['username']
            succ_msg = request.session['succ_msg']
        except KeyError:
            username = ''
            succ_msg = ''

        # 与课程章节相同部分
        course = Course.objects.get(id=course_id)
        org_id = course.courseorg.id
        org = CourseOrg.objects.get(id=org_id)
        teacher = org.teacher_set.first()
        download_res = get_list_or_404(CourseResource)

        # 根据用户课程ID，查询出收藏过该课程的用户及其收藏的课程
        usercourse = UserCourse.objects.filter(course=course_id).first()
        if usercourse:
            user = usercourse.user
            course_id_list = UserCourse.objects.filter(user=user).values_list('course')
            usercourse_list = Course.objects.filter(id__in=course_id_list)[:3]
            # print(usercourse_list)
        else:
            usercourse_list = []

        # 查询出课程评论
        comments = CourseComment.objects.filter(course=course_id).order_by('-id')

        # 消息数
        msg_counts = UserMessage.objects.filter(user=request.user.id, has_read=False).count()

        return render(request, 'course/course-comment.html', context={
            'username': username,
            'succ_msg': succ_msg,
            'course_id': course_id,
            'course': course,
            'download_res': download_res,
            'teacher': teacher,
            'usercourse_list': usercourse_list,
            'comments': comments,
            'msg_counts': msg_counts,
        })


class CourseAddCommentView(View):
    """
    发表评论
    """

    def post(self, request):
        # 如果未登录
        if not request.user.is_authenticated:
            return JsonResponse({"status": "fail", "msg": "用户未登录"})

        course_id = request.POST.get('course_id', 0)
        comment = request.POST.get('comment', '')
        if int(course_id) > 0 and comment:
            # 保存评论
            course = get_object_or_404(Course, id=int(course_id))
            user = request.user
            CourseComment.objects.create(user=user, course=course, comment=comment)
            return JsonResponse({"status": "success", "msg": "评论成功"})
        else:
            return JsonResponse({"status": "fail", "msg": "评论失败"})
