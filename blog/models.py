from django.db import models
from user.models import UserInfo
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
# Create your models here.


class Type(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Articles(models.Model):
    title = models.CharField(max_length=40)
    # content = RichTextField()
    content = RichTextUploadingField()
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    author = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    is_public = models.IntegerField(default=1)
    views = models.IntegerField(default=1)
    write_time = models.DateTimeField()
    is_delete = models.IntegerField(default=0)

    def __str__(self):
        return self.title
