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

    choice = models.ForeignKey(Choice)

    def __unicode__(self):
        return unicode(self.email)
