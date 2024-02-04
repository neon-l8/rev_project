from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

