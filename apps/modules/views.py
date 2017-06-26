from django.shortcuts import render, HttpResponse, redirect
from django.views import View

from .models import Articles

# Create your views here.


class ModuleView(View):
    def get(self, request, nid):
        nid = int(nid)
        if nid != 1:
            articles_obj = Articles.objects.filter(module_id=nid)
            return render(request, 'modules.html', {'articles_obj': articles_obj})
        return redirect('/')

