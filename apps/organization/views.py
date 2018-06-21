from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from apps.organization.models import CityDict, CourseOrg
from pure_pagination import Paginator, PageNotAnInteger


class OrgListView(View):
    """
    课程机构列表
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

        # 城市筛选
        city_id = request.GET.get('city', '')
        if city_id:
            all_org = all_org.filter(city_id=int(city_id))

        # 机构分类筛选
        category = request.GET.get('category', '')
        if category:
            all_org = all_org.filter(category=category)

        # 排序筛选
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_org = all_org.order_by('-students')
        if sort == 'courses':
            all_org = all_org.order_by('-courses')

        org_nums = all_org.count()

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_org, 4, request=request)
        page_obj = p.page(page)

        return render(request, 'org-list.html', context={
            'all_city': all_city,
            'username': username,
            'succ_msg': succ_msg,
            'page_obj': page_obj,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'hot_org': hot_org,
            'sort': sort,
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
        courses = course_org.course_set.all()[:2]
        teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', context={
            'username': username,
            'succ_msg': succ_msg,
            'course_org': course_org,
            'courses': courses,
            'teachers': teachers,
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
        courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', context={
            'username': username,
            'succ_msg': succ_msg,
            'course_org': course_org,
            'courses': courses,
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
        return render(request, 'org-detail-desc.html', context={
            'username': username,
            'succ_msg': succ_msg,
            'course_org': course_org,
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
        teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-teachers.html', context={
            'username': username,
            'succ_msg': succ_msg,
            'course_org': course_org,
            'teachers': teachers,
        })

