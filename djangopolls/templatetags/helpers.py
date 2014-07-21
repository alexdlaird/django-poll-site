from django import template

register = template.Library()


@register.filter
def get_from_dict(l, i):
    try:
        return l[i]
    except:
        return None