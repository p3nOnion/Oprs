"""Opra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
import Core.views  as core
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',login_required(core.Main.as_view()) ,name='Core'),
    path('opra/', include('Core.urls'), name='Core'),
    path('accounts/', include('Users.urls'), name='Users'),
    path('terminal/', include('Terminal.urls'), name='Terminal'),
    path('gvm/', include('GVM.urls'), name='Gvm'),
]

admin.site.site_header = "OPRA Admin"
admin.site.site_title = "OPRA Admin Portal"
admin.site.index_title = "Welcome to OPRA Researcher Portal"