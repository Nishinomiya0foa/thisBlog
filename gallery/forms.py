from django import forms
from django.forms import widgets as wid

from .models import Pic


class PicModelForm(forms.ModelForm):
    class Meta:
        model = Pic
        fields = ['name', 'introduction', 'picture', 'type']

        labels = {
            'name': '名称',
            'introduction': '简介',
            'picture': '图片',
            'type': '分类'
        }

        widgets = {
            'name': wid.TextInput(attrs={'class': 'form-control'}),
            'introduction': wid.Textarea(attrs={'cols': 20, 'rows': 2}),
            'picture': wid.FileInput(attrs={'class': 'form-control'})
        }