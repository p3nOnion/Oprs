from django.contrib.auth.decorators import login_required
from django.urls import path, include


from . import views as terminalView
from . import views
urlpatterns = [
    path('', login_required(views.Index.as_view())),
]