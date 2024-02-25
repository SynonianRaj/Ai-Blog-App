import readtime

from django import template
from ..models import Posts
import  markdown as md
from django.template.defaultfilters import stringfilter

register = template.Library()

def timeFormatter(time):  # sourcery skip: avoid-builtin-shadow
    time = tuple(map(int,str(time).split(':')))
    
    hour = time[0]
    min = time[1]
    sec = time[2]
    s = ""
    if hour <=  0:
        # only minute / minutes
        s += f'{min} {'minutes' if min > 1 else 'minute'} {sec} seconds'
    else:
         s += f'{hour} {'hours' if hour > 1 else 'hour'} {min} minutes and {sec} seconds'

    return f"Estimated reading time {s}"





def read(html):
    t = readtime.of_text(html)
    return timeFormatter(t.delta)


register.filter('readtime',read)


@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])
