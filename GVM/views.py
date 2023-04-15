from django.shortcuts import render
from django.views.generic.base import View
import xmltodict
import json
import GVM.GVM.gvm as gvm
from django.http import HttpResponse
import xmltodict
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
# Create your views here.


class Index(View):
    def get(self, request):
        targets = gvm.get_targets()
         
        response = gvm.get_tasks()
        xml_tree = ET.fromstring(response)
        tasks = xml_tree.findall(".//task")
        task_id = [{"name": child.find("name").text, "id": child.attrib['id']}
                   for child in tasks]
        return render(request, 'gvm/index.html', {'response': response, "tasks_id": task_id})
class ActionTask(View):
    def get(self, request, action, id):
        if action =="status":
            response = gvm.get_task(id=id)
            response= ET.fromstring(response)
            status = response.find('task').find("status").text
            return HttpResponse(status)
        elif action == "start":
            response=gvm.start_task(id=id)
            return HttpResponse(response)
        elif action=="stop":
            response=gvm.stop_task(id=id)
            return HttpResponse(response)
        return HttpResponse(status=404)

class TaskDetail(View):
    def get(self, request):
        scancofig = gvm.get_scan_configs()
        scancofig= ET.fromstring(scancofig).findall('config')
        scancofig=[{"id":child.attrib['id'],"name":child.find('name').text} for child in scancofig]

        scanners = gvm.get_scanners()
        scanners= ET.fromstring(scanners).findall('scanner')
        scanners=[{"id":child.attrib['id'],"name":child.find('name').text} for child in scanners]

        targets = gvm.get_targets()
        targets = ET.fromstring(targets).findall('target')
        targets = [{"name": child.find('name').text, "id": child.attrib['id']} for child in targets]

        response = gvm.get_tasks()
        tasks = ET.fromstring(response).findall('task')
        #  them target
        #  them status
        for child in tasks:
            print([x.find('report').attrib for x in child.findall('last_report') if int(child.find('report_count').text) > 0])
        tasks = [{"name": child.find("name").text, "id": child.attrib['id'],"comment":child.find("comment").text,"scanner":child.find('scanner').find('name').text,"config":child.find("config").find('name').text, 'status':child.find("status").text, "report": "None" if len([x.find('report') for x in child.findall('last_report') if int(child.find('report_count').text) > 0])==0 else [x.find('report').attrib['id'] for x in child.findall('last_report') if int(child.find('report_count').text)][0] }
                   for child in tasks]
        print(tasks)
        return render(request, "gvm/task.html",{'scanner_lists':scancofig,"scanners":scanners, "targets":targets, "tasks":tasks})
    def post(self, request):
        name=request.POST.get("name",None)
        config_id= request.POST.get("name",None)
        target_id=request.POST.get("target_id",None)
        scanner_id=request.POST.get("scanner_id",None)
        comment=request.POST.get("comment",None)
        if (config_id and target_id and scanner_id) is not None:
            gvm.create_task(name, config_id, target_id, scanner_id, comment)
        return render(request, "gvm/task.html")
class Target(View):
    def get(self, request):
        targets = gvm.get_targets()
        targets = ET.fromstring(targets).findall('target')
        
        targets = [{"name": child.find('name').text, "id": child.attrib['id'],
        "hosts": child.find('hosts').text, "comment": child.find('comment').text,
        "port_list": child.find('port_list').find('name').text,
        "hosts": child.find('hosts').text,
        "in_use": child.find('in_use').text,
        } for child in targets]


        port_lists = gvm.get_port_lists()
        port_lists = ET.fromstring(port_lists)
        port_lists = port_lists.findall("port_list")
        port_lists_id = [{'name': child.find(
            'name').text, "id": child.attrib['id']} for child in port_lists]


        return render(request, "gvm/target.html", 
        {"port_lists": port_lists_id, "targets":targets})

    def post(self, request):
        print(request.POST)
        name = request.POST.get('name', None)
        comment = request.POST.get("comment", "")
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
        return self.get(request)

    def delete(self, request, id):

        gvm.delete_target(id)

        return self.get(request)

class Task(View):
    def get(self, request, id):
        response = gvm.get_task(id)
        # response = xmltodict.parse(response)
        return render(request, 'gvm/index.html', {'response': response})


class Tasks(View):
    def get(self, request):
        response = gvm.get_tasks()
        response = xmltodict.parse(response)
        return render(request, 'gvm/index.html', {'response': response})


class Result(View):
    def get(self, request, id):
        response = gvm.get_result(id)
        response = ET.fromstring(response)

        result = response.find('result')
        id = result.attrib['id']

    
        # response = response["get_results_response"]

        return render(request, 'gvm/result.html', {'response': gvm.get_result(id)})


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
