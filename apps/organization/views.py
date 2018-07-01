from django.db.models import Q
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic.base import View

from apps.operation.models import UserFavorite, UserMessage
from apps.organization.models import CityDict, CourseOrg, Teacher
from pure_pagination import Paginator, PageNotAnInteger


class OrgListView(View):
    """
    授课机构导航列表
    """

    def get(self, request):
        try:
            username = request.session['username']
            succ_msg = request.session['succ_msg']
        except KeyError:
            username = ''
            succ_msg = ''

        all_city = CityDict.objects.all()
        all_org = CourseOrg.objects.all()

        hot_org = CourseOrg.objects.order_by('-click_nums')[:3]  # 用于机构排行

        # 搜索机构
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_org = all_org.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords))

        # 城市筛选
        city_id = request.GET.get('city', '')
        if city_id:
            all_org = all_org.filter(city_id=int(city_id))

        # 机构分类筛选
        category = request.GET.get('category', '')
        if category:
            all_org = all_org.filter(category=category)

        # 排序
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_org = all_org.order_by('-students')
        if sort == 'courses':
            all_org = all_org.order_by('-courses')

        org_nums = all_org.count()

        # 消息数
        msg_counts = UserMessage.objects.filter(user=request.user.id, has_read=False).count()

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_org, 4, request=request)
        page_obj = p.page(page)

        return render(request, 'org/org-list.html', context={
            'all_city': all_city,
            'username': username,
            'succ_msg': succ_msg,
            'page_obj': page_obj,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'hot_org': hot_org,
            'sort': sort,
            'keywords': keywords,
            'msg_counts': msg_counts,
        })


class OrgHomeView(View):
    """
    机构首页
    """

    def get(self, request, org_id):
        try:
            username = request.session['username']
            succ_msg = request.session['succ_msg']
        except KeyError:
            username = ''
            succ_msg = ''

        course_org = CourseOrg.objects.get(id=int(org_id))

        # 判断是否收藏
        is_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                is_fav = True

        courses = course_org.course_set.all()[:2]
        teachers = course_org.teacher_set.all()[:1]

        # 消息数
        msg_counts = UserMessage.objects.filter(user=request.user.id, has_read=False).count()

        return render(request, 'org/org-detail-homepage.html', context={
            'username': username,
            'succ_msg': succ_msg,
            'course_org': course_org,
            'courses': courses,
            'teachers': teachers,
            'is_fav': is_fav,
            'msg_counts': msg_counts,
        })


class OrgCourseView(View):
    """
    机构课程
    """

    def get(self, request, org_id):
        try:
            username = request.session['username']
            succ_msg = request.session['succ_msg']
        except KeyError:
            username = ''
            succ_msg = ''

        course_org = CourseOrg.objects.get(id=int(org_id))

        # 判断是否收藏
        is_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                is_fav = True

        courses = course_org.course_set.all()

        # 消息数
        msg_counts = UserMessage.objects.filter(user=request.user.id, has_read=False).count()

        return render(request, 'org/org-detail-course.html', context={
            'username': username,
            'succ_msg': succ_msg,
            'course_org': course_org,
            'courses': courses,
            'is_fav': is_fav,
            'msg_counts': msg_counts,
        })


class OrgDescView(View):
    """
    机构介绍
    """
    def get(self, request, org_id):
        try:
            username = request.session['username']
            succ_msg = request.session['succ_msg']
        except KeyError:
            username = ''
            succ_msg = ''

        course_org = CourseOrg.objects.get(id=int(org_id))

        # 判断是否收藏
        is_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                is_fav = True

        # 消息数
        msg_counts = UserMessage.objects.filter(user=request.user.id, has_read=False).count()

        return render(request, 'org/org-detail-desc.html', context={
            'username': username,
            'succ_msg': succ_msg,
            'course_org': course_org,
            'is_fav': is_fav,
            'msg_counts': msg_counts,
        })


class OrgTeacherView(View):
    """
    机构教师
    """
    def get(self, request, org_id):
        try:
            username = request.session['username']
            succ_msg = request.session['succ_msg']
        except KeyError:
            username = ''
            succ_msg = ''

        course_org = CourseOrg.objects.get(id=int(org_id))

        # 判断是否收藏
        is_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                is_fav = True

        teachers = course_org.teacher_set.all()

        # 消息数
        msg_counts = UserMessage.objects.filter(user=request.user.id, has_read=False).count()

        return render(request, 'org/org-detail-teachers.html', context={
            'username': username,
            'succ_msg': succ_msg,
            'course_org': course_org,
            'teachers': teachers,
            'is_fav': is_fav,
            'msg_counts': msg_counts,
        })


class TeacherListView(View):
    """
    授课教师导航列表
    """
    def get(self, request):
        try:
            username = request.session['username']
            succ_msg = request.session['succ_msg']
        except KeyError:
            username = ''
            succ_msg = ''

        all_teachers = Teacher.objects.all()
        teacher_nums = all_teachers.count()

        hot_teacher = Teacher.objects.all().order_by('-fav_nums')[:2]

        # 搜索教师
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_teachers = all_teachers.filter(name__icontains=keywords)

        # 人气排序
        sort = request.GET.get('sort', '')
        if sort == 'popu':
            all_teachers = all_teachers.order_by('-click_nums')

        # 消息数
        msg_counts = UserMessage.objects.filter(user=request.user.id, has_read=False).count()

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 3, request=request)
        page_obj = p.page(page)

        return render(request, 'org/teachers-list.html', context={
            'username': username,
            'succ_msg': succ_msg,
            'page_obj': page_obj,
            'teacher_nums': teacher_nums,
            'sort': sort,
            'hot_teacher': hot_teacher,
            'keywords': keywords,
            'msg_counts': msg_counts,
        })


class TeacherDetailView(View):
    """
    讲师详情页
    """
    def get(self, request, teacher_id):
        try:
            username = request.session['username']
            succ_msg = request.session['succ_msg']
        except KeyError:
            username = ''
            succ_msg = ''

        teacher = get_object_or_404(Teacher, pk=teacher_id)
        courses = teacher.course_set.all()

        hot_teacher = Teacher.objects.all().order_by('-fav_nums')[:2]

        # 判断是否收藏
        is_fav_teacher = False
        is_fav_org = False
        org_id = teacher.org.id
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher_id, fav_type=3):
                is_fav_teacher = True
            if UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=2):
                is_fav_org = True

        # 消息数
        msg_counts = UserMessage.objects.filter(user=request.user.id, has_read=False).count()

        return render(request, 'org/teacher-detail.html', context={
            'username': username,
            'succ_msg': succ_msg,
            'teacher': teacher,
            'courses': courses,
            'hot_teacher': hot_teacher,
            'is_fav_teacher': is_fav_teacher,
            'is_fav_org': is_fav_org,
            'org_id': org_id,
            'msg_counts': msg_counts,
        })


