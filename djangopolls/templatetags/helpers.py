"""
Believe it or not, there are some things even Django can't do when it comes to its template
language syntax. And for that, you just write your own. Problem solved.

For our example below, Django is able to index a list in a template, but not a dictionary, so
our filter simply takes a dictionary and an argument of a key for the lookup. The syntax in
the template to use this filter would be similar to "someList|get_from_dict:key".

And before you get a serious headache wondering why this won't work, you'll need to add
"django.core.context_processors.request" to your list of TEMPLATE_CONTEXT_PROCESSORS in
settings.py before your template will be able to find this tag.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/custom-template-tags/
"""

from django import template

register = template.Library()


@register.filter
def get_from_dict(list, key):
    try:
        return list[key]
    except:
        return None