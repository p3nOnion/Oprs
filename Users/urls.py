# accounts/urls.py
from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from .views import Login_view, Register_user,About_view
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('login/', Login_view.as_view(), name="login"),
    path('about/', login_required(About_view.as_view()), name="about"),
    path('register/', Register_user.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
