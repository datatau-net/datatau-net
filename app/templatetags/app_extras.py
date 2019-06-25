from django import template
# import markdown as md

register = template.Library()
from django.template.defaultfilters import stringfilter


@register.filter(name='add_arg')
def add_arg(_1, _2):
    return _1, _2


# @register.filter(name='markdown')
# @stringfilter
# def markdown(value):
#     return md.markdown(value, extensions=['markdown.extensions.fenced_code'])
