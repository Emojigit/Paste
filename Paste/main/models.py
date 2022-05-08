from django.db import models

# Create your models here.

class Paste(models.Model):
    description = "Pastes"
    title = models.CharField(max_length=50)
    access_token = models.CharField(max_length=10) # http://server/<int:id>-<str:access_token>/
    delete_token = models.CharField(max_length=10) # http://server/d/<int:id>-<str:delete_token>/
    content = models.TextField()
    time = models.DateTimeField(auto_now_add = True,editable=False)

class Ban(models.Model):
    description = "Banned Words"
    keyword = models.CharField(max_length=20,unique=True)
    enabled = models.BooleanField(default=True)

