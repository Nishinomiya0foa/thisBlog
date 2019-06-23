from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets as wid

from .models import UserInfo


class UserModelForm(forms.ModelForm):
    username = forms.CharField(max_length=20,
                               min_length=8,)
    r_password = forms.CharField(max_length=20,
                                 min_length=5,
                                 label='确认密码',
                                 error_messages={'require': '密码不得为空!'},
                                 widget=wid.PasswordInput())

    class Meta:
        model = UserInfo
        fields = ['username', 'gender', 'email', 'password', 'r_password']

        labels = {
            'gender': '性别',
        }

        widgets = {
            'password': wid.PasswordInput,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        pwd = self.cleaned_data.get("password")
        r_pwd = self.cleaned_data.get("r_password")  # 娶不到值就是None

        if pwd == r_pwd:
            return self.cleaned_data  # 返回值必须是这个, 或者抛出异常
        else:
            raise ValidationError('两次密码不一致!')
