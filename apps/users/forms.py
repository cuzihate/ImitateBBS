# /usr/bin/env python
# coding:utf-8
# author:ZhaoHu

from django import forms
from django.forms import fields
from django.forms import widgets
from django.core.exceptions import ValidationError

from .models import UserProfile, EmailVerifyRecord


class BaseForm(forms.Form):
    password = fields.CharField(
        required=True,
        widget=widgets.PasswordInput,
        error_messages={
            'required': '密码不能为空',
        }
    )
    email = fields.EmailField(
        required=True,
        error_messages={
            'required': '邮箱不能为空',
            'invalid': '邮箱格式错误'
        }
    )


class LoginForm(BaseForm):
    def clean(self):
        user = UserProfile.objects.filter(email=self.cleaned_data.get('email'), password=self.cleaned_data.get('password')).count()
        if user:
            return self.cleaned_data
        else:
            raise ValidationError('用户名或密码错误')


class SendEmailForm(forms.Form):
    email = fields.EmailField(
        required=True,
        error_messages={
            'required': '邮箱不能为空',
            'invalid': '邮箱格式错误'
        }
    )

    def clean(self):
        user_base = UserProfile.objects.filter(email=self.cleaned_data.get('email')).count()
        if not user_base:
            return self.cleaned_data
        else:
            raise ValidationError('邮箱已存在，请更换！')


class RegisterForm(BaseForm):
    code = fields.CharField(
        required=True,
        error_messages={
            'required': '验证码不能为空',
            'invalid': '验证码错误'
        }
    )

    def clean(self):
        # UserProfile.objects.get(xx=xx).id
        uid = UserProfile.objects.get(email=self.cleaned_data.get('email')).id
        current_user = EmailVerifyRecord.objects.filter(email_id=uid, code=self.cleaned_data.get('code')).count()
        if current_user:
            return self.cleaned_data
        else:
            raise ValidationError('邮箱与验证码不匹配！')
