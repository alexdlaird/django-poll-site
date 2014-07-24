"""
Huzzah, you've found the Django ORM! There's a ton that could be said here, so let's keep it simple.
Classes in this file need to extend django.db.models.Model. Think of a class as a table in the database,
and think of an object (an instantiation of a class below) as a row within that table.

Here, we'll get you started. When you want to get a specific poll, say from a function in views.py, do
something like the following:

from djangopolls.models import Poll
poll = Poll.objects.get(question='This is the text of the question')

Boom. Now play around with that "poll" variable, and look into "filter" instead of "get" if you'd like
to retrieve a slew of results.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/db/models/
"""

from django.db import models
from django.utils import timezone

from djangopolls.utils import generate_slug


class Poll(models.Model):
    question = models.CharField(max_length=256)
    subtext = models.CharField(max_length=256, blank=True, null=True)
    open_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    close_date = models.DateTimeField(default=None, blank=True, null=True)
    is_annonymous = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.question)


class Choice(models.Model):
    answer = models.CharField(max_length=256)

    poll = models.ForeignKey(Poll)

    def __unicode__(self):
        return unicode(self.answer)


class Vote(models.Model):
    email = models.EmailField(max_length=256)
    validation_slug = models.SlugField(default=generate_slug, blank=True, null=True, unique=True)
    accepted = models.BooleanField(default=False)

    choice = models.ForeignKey(Choice)

    def __unicode__(self):
        return unicode(self.email)
