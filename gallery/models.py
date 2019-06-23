from django.db import models

from user.models import UserInfo

# Create your models here.


class Type(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Pic(models.Model):
    name = models.CharField(max_length=40)
    introduction = models.CharField(max_length=140)
    picture = models.ImageField(upload_to="%Y/%m/%d/")
    author = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    is_public = models.IntegerField(default=1)
    write_time = models.DateTimeField()
    is_delete = models.IntegerField(default=0)

    def __str__(self):
        return self.name