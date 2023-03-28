from django.db import models

# Create your models here.
class Exploit(models.Model):
    name = models.CharField(max_length=200)
    os  = models.CharField(max_length=200)
    module = models.CharField(max_length=200)
    payload = models.CharField(max_length=200)
    uri = models.CharField(max_length=200,default=None)
    rhost = models.CharField(max_length=200)
    rport = models.IntegerField()
    lhost =models.CharField(max_length=200, default=None)
    lport = models.IntegerField(default=None)


