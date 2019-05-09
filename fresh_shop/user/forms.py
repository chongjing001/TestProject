import re

from django import forms
from django.contrib.auth.hashers import check_password

from user.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=5, required=True,
                               error_messages={
                                   'required': '用户名必填',
                                   'max_length': '用户名不能超过20个字符',
                                   'min_length': '用户名不能少于5个字符'
                               })
    pwd = forms.CharField(max_length=20, min_length=5, required=True,
                          error_messages={
                              'required': '密码必填',
                              'max_length': '密码不能超过',
                              'min_length': ''
                          })

    cpwd = forms.CharField(max_length=20, min_length=5, required=True,
                           error_messages={
                               'required': '密码必填',
                               'max_length': '',
                               'min_length': ''
                           })
    email = forms.CharField(required=True,
                            error_messages={
                                'required': '邮箱必填',
                            })
    allow = forms.BooleanField(required=True,
                               error_messages={
                                   'required': '必须同意协议'
                               })

    def clean_user_name(self):
        # 校验注册的账号是否存在啊
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).first()
        if user:
            raise forms.ValidationError('该账号已存在，请更换账号注册')
        return self.cleaned_data['username']

    def clean(self):
        pwd = self.cleaned_data.get('pwd')
        cpwd = self.cleaned_data.get('cpwd')
        if pwd != cpwd:
            raise forms.ValidationError({'cpwd': '两次密码不一致'})
        return self.cleaned_data

    def clean_email(self):
        # 校验邮箱格式
        email_reg = '^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$'
        email = self.cleaned_data['email']
        if not re.match(email_reg, email):
            raise forms.ValidationError('邮箱格式错误')
        return self.cleaned_data['email']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=5, required=True,
                               error_messages={
                                   'required': '用户名必填',
                                   'max_length': '用户名不能超过20个字符',
                                   'min_length': '用户名不能少于5个字符'
                               })
    pwd = forms.CharField(max_length=20, min_length=5, required=True,
                          error_messages={
                              'required': '密码必填',
                              'max_length': '密码不能超过',
                              'min_length': ''
                          })

    def clean(self):
        # 校验用户名是否注册
        username = self.cleaned_data.get('username')
        print(username)
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError({'username': '该账号没有注册'})
        password = self.cleaned_data.get('pwd')
        print(password)
        if not check_password(password, user.password):
            raise forms.ValidationError({'pwd': '密码错误'})
        return self.cleaned_data


class AddressForm(forms.Form):
    username = forms.CharField(max_length=5, required=True,
                               error_messages={
                                   'required': '收件人必填'
                               })
    address = forms.CharField(required=True,
                              error_messages={
                                  'required': '地址必填'
                              })

    postcode = forms.CharField(required=True,
                               error_messages={
                                   'required': '邮箱必填'
                               })
    mobile = forms.CharField(required=True,
                             error_messages={
                                 'required': '手机号必填'
                             })
