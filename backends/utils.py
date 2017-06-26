# /usr/bin/env python
# coding:utf-8
# author:ZhaoHu

from django.core.exceptions import ValidationError
from django.core.mail import send_mail

import json
import random

from users.models import EmailVerifyRecord, UserProfile
from ImitateBBS.settings import EMAIL_FROM



class JsonCustomEncoder(json.JSONEncoder):
    def default(self, field):
        if isinstance(field, ValidationError):
            return {'code': field.code, 'messages': field.messages}
        else:
            return json.JSONEncoder.default(self, field)


def random_str(random_len=8):
    rand_str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for _ in range(random_len):
        rand_str += chars[random.randint(0, length)]
    return rand_str

def send_register_email(email, send_type='register'):
    exist_email = UserProfile.objects.filter(email=email).count()
    if not exist_email:
        user_record = UserProfile()
        user_record.email = email
        user_record.save()
    email_record = EmailVerifyRecord()
    email_record.email_id = UserProfile.objects.get(email=email).id
    code = random_str(6)
    email_record.code = code
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        email_title = '仿抽屉BBS注册验证码'
        email_body = '您本次的验证码为：{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            print('已发送，请注意查收！')