from django.contrib.auth.decorators import login_required
from django.urls import path, include, re_path


from . import views as core

urlpatterns = [
    path('', login_required(core.Main.as_view()), name='Terminal'),
    path('auto/<str:id1>/', login_required(core.Auto.as_view(), "Auto")),
    path("sessions/", login_required(core.LoadSessions.as_view()), name='Sesssions'),
    path("sessions/<int:id>",
         login_required(core.LoadSessionId.as_view()), name='SesssionsId'),
    path("msf/<int:id>", login_required(core.Msf.as_view()), name='Metasploit'),
    path("info/<str:ip>", login_required(core.Info.as_view()), name='Info'),
    path("exploit/", login_required(core.Module.as_view()), name="Module"),
    path("report_metasploit/", login_required(core.ReportMetasploit.as_view()), name="Report_Metasploit"),
    path("report_metasploit/<str:ip>", login_required(core.ReportMetasploitByIp.as_view()), name="Report_MetasploitByIp"),
    path("meterpreter/<int:id>",
         login_required(core.Meterpreter.as_view()), name="Meterpreter"),
    path("message/", login_required(core.Message.as_view()), name="Message")
]
