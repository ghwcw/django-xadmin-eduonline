from django.shortcuts import render, get_object_or_404, get_list_or_404

# Create your views here.
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger

from apps.course.models import Course, CourseResource
from apps.operation.models import UserFavorite
from apps.organization.models import CourseOrg


class CourseListView(View):
    """
    课程列表页
    """
    def get(self, request):
        try:
            username = request.session['username']
            succ_msg = request.session['succ_msg']
        except KeyError:
            username = ''
            succ_msg = ''

        all_courses = Course.objects.all().order_by('-add_time')

        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        # 筛选排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_courses, 6, request=request)
        page_obj = p.page(page)

        return render(request, 'course-list.html', context={
            'username': username,
            'succ_msg': succ_msg,
            'page_obj': page_obj,
            'sort': sort,
            'hot_courses': hot_courses,
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
            org_id = course.courseorg.id
            if UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=2):
                is_fav_org = True

        return render(request, 'course-detail.html', context={
            'username': username,
            'succ_msg': succ_msg,
            'course': course,
            'relate_course': relate_course,
            'is_fav_course': is_fav_course,
            'is_fav_org': is_fav_org,
        })


class CourseVideoView(View):
    """
    课程章节（视频）
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

        print(teacher)

        return render(request, 'course-video.html', context={
            'username': username,
            'succ_msg': succ_msg,
            'course_id': course_id,
            'course': course,
            'download_res': download_res,
            'teacher': teacher,
        })

