from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from apps.organization.models import CityDict


class OrgListView(View):
    """
    课程机构列表
    """
    def get(self, request):
        username = request.session['username']
        succ_msg = request.session['succ_msg']
        all_city = CityDict.objects.all()
        return render(request, 'org-list.html', context={'all_city': all_city, 'username': username, 'succ_msg': succ_msg})

