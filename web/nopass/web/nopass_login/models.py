from django.db import models

class Account(models.Model):
    token = models.CharField(max_length=200, unique=True)
    username = models.CharField(max_length=50, unique=True)
    is_admin = models.BooleanField(default=False)
