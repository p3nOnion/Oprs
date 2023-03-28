from django.contrib import admin
from .models import Exploit
# Register your models here.
class CustomExploitAdmin():
    model = Exploit
    list_display = ['name', 'os']


admin.site.register(Exploit)