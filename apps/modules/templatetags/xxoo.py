# /usr/bin/env python
# coding:utf-8
# author:ZhaoHu


from django import template

register = template.Library()

@register.filter
def for_in(arg1, list1):
    if arg1 in list1:
        return True
    return False
