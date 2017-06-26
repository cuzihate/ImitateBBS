# coding:utf-8

from django.db import models


# Create your models here.

class UserProfile(models.Model):
    username = models.CharField(max_length=20, verbose_name='用户名', unique=True, null=True, blank=True)
    password = models.CharField(max_length=20, verbose_name='密码', null=True, blank=True)
    email = models.EmailField('邮箱', unique=True)
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(('male', '男'), ('female', '女')), default='male')
    mobile = models.CharField(max_length=11, verbose_name='手机号', null=True, blank=True)
    image = models.ImageField(upload_to='static/image/%Y/%m', default='static/image/default.png', verbose_name='用户头像')
    address = models.CharField(max_length=50, default='', verbose_name='地址信息', null=True, blank=True)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    email = models.ForeignKey('UserProfile', verbose_name='邮箱')
    code = models.CharField(max_length=20, verbose_name='验证码')
    send_type = models.CharField(max_length=10, choices=(('register', '注册'), ('forget', '找回')), verbose_name='验证码类型')
    send_time = models.DateTimeField(auto_now=True, verbose_name='发送时间')

    class Meta:
        verbose_name = '邮箱验证'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.email.email


