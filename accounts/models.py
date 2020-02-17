from django.contrib.auth.models import AbstractUser

from django.db import models


class CustomUser(AbstractUser):
    karma = models.IntegerField(default=1)
    about = models.TextField(default='')
    api_key = models.CharField(max_length=100)
    is_troll = models.BooleanField(default=False)
