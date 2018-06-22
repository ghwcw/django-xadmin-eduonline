from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger

from apps.course.models import Course


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
