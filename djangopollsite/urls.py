"""
Here you use regular expressions to define the URLs that your application will accept, and you
pair those to a Python function that you've defined in your views.py file.

Here's the skinny: at the end of the day, you need to assign a variable named "urlpatterns" a list
of django.conf.urls.ulr() instances. If your project is going to be abstracted into numerous apps,
you'll probably want to look into the "include" functionality to abstract URL definitions to their
appropriate places.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/http/urls/
"""

from django.conf.urls import patterns, include, url
from django.contrib import admin

from djangopolls.admin import django_polls_admin_site

urlpatterns = [
               url(r'^admin/', include(django_polls_admin_site.urls)),
               url(r'^$', 'djangopolls.views.home'),
               url(r'^polls$|^poll$', 'djangopolls.views.home'),
               url(r'^poll/([0-9]+)$', 'djangopolls.views.poll'),
               url(r'^poll/([0-9]+)/vote$', 'djangopolls.views.vote'),
]