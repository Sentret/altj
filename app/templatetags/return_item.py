from django import template
from django.db import models


register = template.Library()

@register.filter
def return_item(l, i):
    try:
        return l[i]
    except:
        return ''