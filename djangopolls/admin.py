from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.conf import settings

from djangopolls.models import Poll, Choice

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2014, Alex Laird'
__version__ = '0.0.1'


class DjangoPollsAdminSite(AdminSite):
    """
    Custom admin site for the Helium app.
    """
    site_header = settings.SITE_TITLE + ' Administration'
    site_title = site_header
    index_title = settings.SITE_TITLE

django_polls_admin_site = DjangoPollsAdminSite()


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question', 'subtext', 'open_date', 'close_date', 'is_annonymous']}),
    ]
    inlines = [ChoiceInline]


django_polls_admin_site.register(User)
django_polls_admin_site.register(Poll, PollAdmin)