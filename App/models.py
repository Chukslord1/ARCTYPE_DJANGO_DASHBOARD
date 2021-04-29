from django.db import models
import datetime

# Create your models here.
class PageView(models.Model):
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40)
    created = models.DateTimeField(default=datetime.datetime.now())

class LogoutRegister(models.Model):
    username = models.TextField()
    created = models.DateTimeField(default=datetime.datetime.now())
