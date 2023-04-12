from django.shortcuts import render
from django.views.generic.base import View
import xmltodict
import json
import GVM.GVM.gvm as gvm
import xmltodict
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
# Create your views here.


class Index(View):
    def get(self, request):
        response = gvm.get_tasks()
        xml_tree = ET.fromstring(response)
        tasks = xml_tree.findall(".//task")
        task_id = [{"name": child.find("name").text, "id": child.attrib['id']}
                   for child in tasks]
        return render(request, 'gvm/index.html', {'response': response, "tasks_id": task_id})


class Task(View):
    def get(self, request, id):
        response = gvm.get_task(id)
        response = xmltodict.parse(response)
        return render(request, 'gvm/index.html', {'response': response})


class Tasks(View):
    def get(self, request):
        response = gvm.get_tasks()
        response = xmltodict.parse(response)
        return render(request, 'gvm/index.html', {'response': response})


class Result(View):
    def get(self, request, id):
        response = gvm.get_result(id)
        response = xmltodict.parse(response)
        print(type(response))
        response = response["get_results_response"]

        return render(request, 'gvm/index.html', {'response': response})


class Results(View):
    def get(self, request):
        response = gvm.get_results()
        response = xmltodict.parse(response)
        return render(request, 'gvm/index.html', {'response': response})
