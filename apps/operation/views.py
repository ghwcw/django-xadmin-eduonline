from django.http import HttpResponse

# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import View

from apps.course.models import Course
from apps.operation.forms import UserAskForm
from apps.operation.models import UserFavorite, UserCourse, UserMessage
from apps.organization.models import CourseOrg, Teacher


class UserAskView(View):
    """
    用户咨询
    交给JS进行异步处理，然后给视图处理，最后视图返回给JS某些数据（JS接受json数据）
    """

    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "errmsg":"填写数据格式有误"}',
                                content_type='application/json')


class AddFavView(View):
    """
    收藏或删除收藏
    """

    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        fav_id = int(fav_id)
        fav_type = int(fav_type)

        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        else:
            # 查询收藏表和用户课程表是否存在记录
            exist_fav_rec = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
            exist_usercourse_rec = UserCourse.objects.filter(user=request.user, course_id=fav_id)
            if exist_fav_rec or exist_usercourse_rec:
                exist_fav_rec.delete()
                exist_usercourse_rec.delete()

                # 收藏数减1
                if fav_type == 1:
                    course = get_object_or_404(Course, id=fav_id)
                    course.fav_nums -= 1
                    if course.fav_nums < 0: course.fav_nums = 0
                    course.save()
                elif fav_type == 2:
                    org = get_object_or_404(CourseOrg, id=fav_id)
                    org.fav_nums -= 1
                    if org.fav_nums < 0: org.fav_nums = 0
                    org.save()
                elif fav_type == 3:
                    teacher = get_object_or_404(Teacher, id=fav_id)
                    teacher.fav_nums -= 1
                    if teacher.fav_nums < 0: teacher.fav_nums = 0
                    teacher.save()

                return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
            else:
                if fav_id > 0 and fav_type > 0:
                    user_fav = UserFavorite()
                    user_fav.user = request.user
                    user_fav.fav_id = fav_id
                    user_fav.fav_type = fav_type
                    user_fav.save()

                    # 收藏后记录消息
                    if fav_type == 1:
                        course = get_object_or_404(Course, id=fav_id)
                        UserMessage.objects.create(user=request.user.id, message='您收藏了课程《%s》' % course.name,
                                                   has_read=False)
                        course.fav_nums += 1  # 收藏数加1
                        course.save()
                    elif fav_type == 2:
                        org = get_object_or_404(CourseOrg, id=fav_id)
                        UserMessage.objects.create(user=request.user.id, message='您收藏了机构“%s”' % org.name,
                                                   has_read=False)
                        org.fav_nums += 1  # 收藏数加1
                        org.save()
                    elif fav_type == 3:
                        teacher = get_object_or_404(Teacher, id=fav_id)
                        UserMessage.objects.create(user=request.user.id, message='您收藏了“%s”老师' % teacher.name,
                                                   has_read=False)
                        teacher.fav_nums += 1  # 收藏数加1
                        teacher.save()

                    # 收藏课程时，保存用户课程记录（用户ID和课程ID）
                    if fav_type == 1:
                        UserCourse.objects.create(user=request.user, course=Course.objects.get(id=fav_id))
                    return HttpResponse('{"status":"success", "msg":"取消收藏"}', content_type='application/json')
                else:
                    return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


# 处理全局404页面
def page_not_found(request):
    return render(request, 'errpage/404.html', status=404)


# 处理全局500页面
def server_error(request):
    return render(request, 'errpage/500.html', status=500)
