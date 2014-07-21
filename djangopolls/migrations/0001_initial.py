# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import djangopolls.utils


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=256)),
                ('subtext', models.CharField(max_length=256, null=True, blank=True)),
                ('open_date', models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True)),
                ('close_date', models.DateTimeField(default=None, null=True, blank=True)),
                ('is_annonymous', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='choice',
            name='poll',
            field=models.ForeignKey(to='djangopolls.Poll'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=256)),
                ('validation_slug', models.SlugField(null=True, default=djangopolls.utils.generate_slug, blank=True, unique=True)),
                ('choice', models.ForeignKey(to='djangopolls.Choice')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
