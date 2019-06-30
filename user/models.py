from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserInfo(AbstractUser):
    """user表新增gender字段"""
    gender = models.IntegerField(choices=((1, '男'), (0, '女')), default=1)

