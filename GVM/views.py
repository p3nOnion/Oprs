from django.shortcuts import render
from django.views.generic.base import View
import GVM.GVM.gvm as gvm 
# Create your views here.
class Index(View):
    def get(self, request):
        response =gvm.get_tasks()
        return render(request, 'gvm/index.html',{'response':response})