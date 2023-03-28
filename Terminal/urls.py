from django.contrib.auth.decorators import login_required
from django.urls import path, include


from . import views as terminalView
from . import views
urlpatterns = [
    path('', login_required(views.index.as_view())),
    path('upload_ssh_key/', views.upload_ssh_key),
]