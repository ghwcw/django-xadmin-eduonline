from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from apps.operation.forms import UserAskForm


class UserAskView(View):
    """
    用户咨询提交给JS进行异步处理（JS接受json数据）
    """

    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "errmsg":"填写数据格式有误"}',
                                content_type='application/json')
