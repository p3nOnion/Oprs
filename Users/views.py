# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from django.views import View

from .forms import LoginForm, SignUpForm

class Login_view(View):
    def get(self, request):
        form = LoginForm(request.POST or None)
        msg = None
        return render(request, "accounts/login.html", {"form": form, "msg": msg})
    def post(self, request):
        print(1)
        form = LoginForm(request.POST or None)
        msg = None
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

        return render(request, "accounts/login.html", {"form": form, "msg": msg})


class Register_user(View):
    def get(self, request):
        msg = None
        success = False
        form = SignUpForm()
        return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})
    def post(self, request):
        msg = None
        success = False
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                msg = 'User created.'
                success = True
        # return redirect("/login/")

        else:
            msg = 'Form is not valid'


        return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})

class About_view(View):
    def get(self, request):
        return render(request, "accounts/about.html")