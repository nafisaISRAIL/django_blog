from django.template import Library
from django.templatetags import static

register = Library()


@register.filter
def get_image(value):
    if value:
        return value.url
    return static('avatar.jpg')
