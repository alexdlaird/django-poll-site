from django.conf.urls import patterns, include, url
from django.contrib import admin

from djangopolls.admin import django_polls_admin_site

urlpatterns = patterns('',
                       url(r'^admin/', include(django_polls_admin_site.urls)),
                       url(r'^$', 'djangopolls.views.home'),
                       url(r'^polls$|^poll$', 'djangopolls.views.home'),
                       url(r'^poll/([a-zA-Z0-9]+)$', 'djangopolls.views.poll'),
                       url(r'^poll/([a-zA-Z0-9]+)/vote$', 'djangopolls.views.vote'),
)
