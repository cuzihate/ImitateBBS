# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-06-25 15:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailVerifyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, verbose_name='验证码')),
                ('send_type', models.CharField(choices=[('register', '注册'), ('forget', '找回')], max_length=10, verbose_name='验证码类型')),
                ('send_time', models.DateTimeField(auto_now=True, verbose_name='发送时间')),
            ],
            options={
                'verbose_name': '邮箱验证',
                'verbose_name_plural': '邮箱验证',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='用户名')),
                ('password', models.CharField(blank=True, max_length=20, null=True, verbose_name='密码')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='邮箱')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='生日')),
                ('gender', models.CharField(choices=[('male', '男'), ('female', '女')], default='male', max_length=10)),
                ('mobile', models.CharField(blank=True, max_length=11, null=True, verbose_name='手机号')),
                ('image', models.ImageField(default='static/image/default.png', upload_to='static/image/%Y/%m', verbose_name='用户头像')),
                ('address', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='地址信息')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
        ),
        migrations.AddField(
            model_name='emailverifyrecord',
            name='email',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserProfile', verbose_name='邮箱'),
        ),
    ]
