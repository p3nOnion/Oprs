from django.shortcuts import render
from django.views.generic.base import View
import xmltodict
import json
import GVM.GVM.gvm as gvm 
# Create your views here.
class Index(View):
    def get(self, request):
        response =gvm.get_tasks()
        return render(request, 'gvm/index.html',{'response':response})
class Task(View):
    def get(self, request, id):
        response = gvm.get_task(id)
        response = xmltodict.parse(response)
        return render(request, 'gvm/index.html',{'response':response})
class Tasks(View):
    def get(self, request):
        response = gvm.get_tasks()
        response = xmltodict.parse(response)
        return render(request, 'gvm/index.html',{'response':response})
class Result(View):
    def get(self, request, id):
        response = gvm.get_result(id)
        response = xmltodict.parse(response)
        return render(request, 'gvm/index.html',{'response':response})
class Results(View):
    def get(self, request):
        response = gvm.get_results()
        response = xmltodict.parse(response)
        return render(request, 'gvm/index.html',{'response':response})