from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'username']


admin.site.register(User, CustomUserAdmin)
