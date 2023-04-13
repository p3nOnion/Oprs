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


class Target(View):
    def get(self, request):
        port_lists = gvm.get_port_lists()
        port_lists = ET.fromstring(port_lists)
        port_lists = port_lists.findall("port_list")
        port_lists_id = [{'name': child.find(
            'name').text, "id": child.attrib['id']} for child in port_lists]
        return render(request, "gvm/target.html", {"port_lists": port_lists_id})

    def post(self, request):
        print(request.POST)
        name = request.POST.get('name', None)
        comment = request.POST.get("name", "")
        hosts = request.POST.get('hosts', None)
        port_lists = request.POST.get("port_lists", None)
        if (name or hosts) is None:
            port_lists = gvm.get_port_lists()
            port_lists = ET.fromstring(port_lists)
            port_lists = port_lists.findall("port_list")
            port_lists_id = [{'name': child.find(
                'name').text, "id": child.attrib['id']} for child in port_lists]
            return render(request, "gvm/target.html", {"port_lists": port_lists_id})
        gvm.create_target(hosts=[hosts], comment=comment,
                          name=name, port_list_id=port_lists)
        targets = gvm.get_targets()
        targets = ET.fromstring(targets).findall('target')
        targets = [{"name": child.find(
            'name').text, "id": child.attrib['id']} for child in targets]
        return render(request, "gvm/target.html", {"targets": targets})


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
        # response = xmltodict.parse(response)
        print(type(response))
        # response = response["get_results_response"]

        return render(request, 'gvm/result.html', {'response': response})


class Results(View):
    def get(self, request):
        response = gvm.get_results()
        response = xmltodict.parse(response)
        return render(request, 'gvm/index.html', {'response': response})


class GetResultByTask(View):
    def get(self, request, id):
        response = gvm.get_task(id=id)
        response = ET.fromstring(response)
        report = response.find('task').find("last_report").find('report')
        response = gvm.get_report(id=report.attrib['id'])
        response = ET.fromstring(response).find('report').find(
            'report').find('results').findall('result')
        response = [child.attrib for child in response]

        return render(request, 'gvm/result.html', {'response': response})


class Report(View):
    def get(self, request, id):
        response = gvm.get_report(id=id)
        return render(request, "gvm/report.html", {"response": response})
