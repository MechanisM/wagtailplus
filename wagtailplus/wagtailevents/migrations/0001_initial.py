# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers
import wagtail.wagtailadmin.taggable


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseEvent',
            fields=[
                ('event_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='schedule.Event')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'ordering': ('-start', 'title'),
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
            bases=('schedule.event', wagtail.wagtailadmin.taggable.TagSearchable),
        ),
    ]
