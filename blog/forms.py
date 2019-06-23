from django import forms
from ckeditor.fields import RichTextField
from django.forms import widgets as wid

from .models import Articles


class ArticleModelForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'type', 'is_public', 'content']

        labels = {
            'title': '标题',
            'content': '正文',
            'type': '分类',
            'is_public': '是否所有人可见',
        }

        error_messages = {
            'title': {'required': '博客标题不能为空'},
            'type': {'required': '博客类别不能为空'},
            'content': {'required': '正文内容不能为空'},
        }

        widgets = {
            'is_public': wid.RadioSelect(choices=(('1', '是'), ('0', '否'))),
            'title': wid.TextInput(attrs={'class': 'form-control'}),
        }


