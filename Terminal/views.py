from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import get_user_model
# Create your views here.
from django.shortcuts import render, HttpResponse
from Terminal.tools.tools import unique
from Opra.settings import TMP_DIR

import os

class index(View):
    def get(self, request):
        return render(request, 'terminal/index.html')


def upload_ssh_key(request):
    if request.method == 'POST':
        pkey = request.FILES.get('pkey')
        ssh_key = pkey.read().decode('utf-8')

        while True:
            filename = unique()
            ssh_key_path = os.path.join(TMP_DIR, filename)
            if not os.path.isfile(ssh_key_path):
                with open(ssh_key_path, 'w') as f:
                    f.write(ssh_key)
                break
            else:
                continue

        return HttpResponse(filename)
