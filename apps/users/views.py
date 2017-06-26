# coding: utf-8

from django.shortcuts import render, HttpResponse, redirect
from django.views import View

import json

from modules.models import Articles, Favour, Comment
from .forms import LoginForm, RegisterForm, SendEmailForm
from users.models import UserProfile, EmailVerifyRecord

from backends.utils import JsonCustomEncoder
from backends.utils import send_register_email

# Create your views here.


class LoginView(View):
    def get(self, request):
        del request.session['email']
        dict_msg = {'state': True}
        return HttpResponse(json.dumps(dict_msg))

    def post(self, request):
        login_obj = LoginForm(request.POST)
        dict_msg = {'state': True}
        if login_obj.is_valid():
            email = login_obj.cleaned_data['email']
            request.session['email'] = email
            return HttpResponse(json.dumps(dict_msg))
        else:
            dict_msg['state'] = False
            dict_msg['errors'] = login_obj.errors.as_data()
            ret = json.dumps(dict_msg, cls=JsonCustomEncoder)
            return HttpResponse(ret)


class SendEmailView(View):
    def post(self, request):
        send_email_obj = SendEmailForm(request.POST)
        dict_msg = {'state': True}
        if send_email_obj.is_valid():
            email = send_email_obj.cleaned_data['email']
            send_register_email(email, 'register')
            return HttpResponse(json.dumps(dict_msg))
        else:
            dict_msg['state'] = False
            dict_msg['errors'] = send_email_obj.errors.as_data()
            ret = json.dumps(dict_msg, cls=JsonCustomEncoder)
            return HttpResponse(ret)


class RegisterView(View):
    def post(self, request):
        register_obj = RegisterForm(request.POST)
        dict_msg = {'state': True}
        if register_obj.is_valid():
            email = register_obj.cleaned_data['email']
            password = register_obj.cleaned_data['password']
            user_profile = UserProfile.objects.get(email=email)
            user_profile.password = password
            user_profile.save()
            return HttpResponse(json.dumps(dict_msg))
        else:
            dict_msg['state'] = False
            dict_msg['errors'] = register_obj.errors.as_data()
            ret = json.dumps(dict_msg, cls=JsonCustomEncoder)
            return HttpResponse(ret)


class IndexView(View):
    def get(self, request):
        articles_obj = Articles.objects.all()
        if request.session.get('email'):
            user_id = UserProfile.objects.filter(email=request.session.get('email')).first().id
            favour_obj = Favour.objects.filter(user_id=user_id)
            favour_ids = [favour.article_id for favour in favour_obj if favour.favour]
            print('当前用户id：{0}, 已点赞表：{1}'.format(user_id, favour_ids))
            return render(request, 'index.html', {'articles_obj': articles_obj, 'user_id': user_id, 'favour_ids': favour_ids})
        return render(request, 'index.html', {'articles_obj': articles_obj})


# 是否登录的装饰器
def check_login(func):
    def inner(self, request, *args, **kwargs):
        if not request.session.get('email'):
            return HttpResponse(json.dumps({'state': False}))
            # state为False表示用户为登录，方便前端逻辑判断
        return func(self, request, *args, **kwargs)
    return inner



class FavourView(View):
    @check_login
    def post(self, request):
        current_article_id = int(request.POST.get('article_id'))
        print(current_article_id, type(current_article_id), request.POST)
        current_email = request.session.get('email')
        current_email_id = UserProfile.objects.filter(email=current_email).first().id
        favour_exist = Favour.objects.filter(user_id=current_email_id, article_id=current_article_id)
        article_obj = Articles.objects.filter(id=current_article_id)
        # 判断favour表里是否已经存在记录且是否点赞
        if favour_exist:
            if favour_exist.first().favour:
                favour_exist.update(favour=False)
                article_obj.update(favour_count=article_obj.first().favour_count - 1)
            else:
                favour_exist.update(favour=True)
                article_obj.update(favour_count=article_obj.first().favour_count + 1)
        # 表记录不存在，直接添加记录
        else:
            favour_obj = Favour()
            favour_obj.user_id = current_email_id
            favour_obj.article_id = int(current_article_id)
            favour_obj.save()
            article_obj.update(favour_count=article_obj.first().favour_count + 1)
        return HttpResponse(json.dumps({'state': True}))


