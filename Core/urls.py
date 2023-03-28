from django.contrib.auth.decorators import login_required
from django.urls import path, include,re_path


from . import views as core

urlpatterns = [
    path('',login_required(core.Main.as_view()) ,name='Terminal'),
    path("sessions/",login_required(core.LoadSessions.as_view()) ,name='Sesssions'),
    path("sessions/<int:id>",login_required(core.LoadSessionId.as_view()) ,name='SesssionsId'),
    path("msf/",login_required(core.Msf.as_view()) ,name='Metasploit'),
]