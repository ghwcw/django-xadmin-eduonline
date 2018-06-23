from django.http import HttpResponse

# Create your views here.
from django.views.generic.base import View

from apps.operation.forms import UserAskForm
from apps.operation.models import UserFavorite


class UserAskView(View):
    """
    用户咨询交给JS进行异步处理，然后给视图处理，最后视图返回给JS某些数据（JS接受json数据）
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
    收藏
    """

    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        fav_id = int(fav_id)
        fav_type = int(fav_type)

        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        else:
            exist_rec = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
            if exist_rec:
                exist_rec.delete()
                return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
            else:
                if fav_id > 0 and fav_type > 0:
                    user_fav = UserFavorite()
                    user_fav.user = request.user
                    user_fav.fav_id = fav_id
                    user_fav.fav_type = fav_type
                    user_fav.save()
                    return HttpResponse('{"status":"success", "msg":"取消收藏"}', content_type='application/json')
                else:
                    return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')
