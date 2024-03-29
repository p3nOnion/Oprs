from django.contrib.auth.decorators import login_required
from django.urls import path, include


from . import views as terminalView
from . import views
urlpatterns = [
    path('', login_required(views.Index.as_view())),
    path('task/<str:id>', login_required(views.Task.as_view())),
    path('tasks/', login_required(views.Tasks.as_view())),
    path('result/<str:id>', login_required(views.Result.as_view())),
    path('results/', login_required(views.Results.as_view())),
]