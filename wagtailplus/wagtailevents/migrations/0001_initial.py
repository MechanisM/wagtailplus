# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers
import wagtail.wagtailadmin.taggable
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('start_date', models.DateField(help_text='Enter the first date of a repeating event, or the date of a one-time event.', verbose_name='Start Date', db_index=True)),
                ('end_date', models.DateField(help_text='Enter the last date of a repeating event, or the date of a one-time event.', verbose_name='End Date', db_index=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text=None, verbose_name='Tags')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
            bases=(models.Model, wagtail.wagtailadmin.taggable.TagSearchable),
        ),
        migrations.CreateModel(
            name='EventFrequency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day_of_week', models.PositiveIntegerField(blank=True, help_text='Event will recur every specified day of the week', null=True, verbose_name='Weekday', choices=[(0, 'Sunday'), (1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday')])),
                ('nth_weekday', models.PositiveIntegerField(blank=True, help_text='Event will recur every nth specified day of the week', null=True, verbose_name='Every Nth Weekday of the Month', choices=[(0, '1st'), (1, '2nd'), (2, '3rd'), (3, '4th')])),
                ('day_of_month', models.PositiveIntegerField(blank=True, help_text='Event will recur every nth day of each month', null=True, verbose_name='Day of Month', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31)])),
                ('day_period', models.PositiveIntegerField(help_text='Event will recur every n number of days', null=True, verbose_name='Day Period', blank=True)),
                ('event', modelcluster.fields.ParentalKey(related_name='frequencies', to='wagtailevents.Event')),
            ],
            options={
                'verbose_name': 'Event Frequency',
                'verbose_name_plural': 'Event Frequencies',
            },
            bases=(models.Model,),
        ),
    ]
